from datetime import datetime, timedelta, timezone
import traceback
import typing as t

from flask import Blueprint, jsonify

from src.consts import YAKU_MAP, IMPORTANT_YAKUS
from src.ms_apis import get_log
from src.validations import validate_log
from src.utils import csv_response

if t.TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

bp = Blueprint("api", __name__)


@bp.route("/uuid-raw/<uuid>")
async def route_uuid_raw(uuid: str) -> "ResponseReturnValue":
    """Serve full Majsoul log as json

    Args:
        uuid (str): uuid of Majsoul log

    Returns:
        ResponseReturnValue: full Majsoul log as json
    """

    data = await get_log(uuid)
    return jsonify(data)


@bp.route("/uuid/<uuid>")
async def route_uuid(uuid: str) -> "ResponseReturnValue":
    """Serve simple Majsoul log as json

    Args:
        uuid (str): uuid of Majsoul log

    Returns:
        ResponseReturnValue: simple Majsoul log as json
    """
    data = await get_log(uuid)
    try:
        is_valid, errors = validate_log(data)
        if not is_valid:
            return (
                jsonify(
                    {
                        "result": "ERROR",
                        "message": "Invalid game log.",
                        "errors": errors,
                        "data": data,
                    }
                ),
                500,
            )

        head = data["head"]

        results = head["result"]["players"]

        # parse for players
        player_ranks = []
        for result in results:
            if "seat" in result:
                seat = result["seat"]
                for player in head["accounts"]:
                    if "seat" in player and player["seat"] == seat:
                        player_ranks.append(
                            {
                                "id": player["accountId"],
                                "seat": seat,
                                "nickname": player["nickname"],
                                "finalPoint": result["partPoint1"],
                            }
                        )
                        break
            else:
                for player in head["accounts"]:
                    if "seat" not in player:
                        player_ranks.append(
                            {
                                "id": player["accountId"],
                                "seat": 0,
                                "nickname": player["nickname"],
                                "finalPoint": result["partPoint1"],
                            }
                        )
                        break

        # set rank by final points
        player_ranks.sort(key=lambda player: player["finalPoint"], reverse=True)
        for i in range(len(player_ranks)):
            player_ranks[i]["rank"] = i + 1

        # parse for noted_yakus
        noted_yakus = []
        for record in data["records"]:
            if record["name"] != "RecordHule":
                continue
            for hule in record["data"]["hules"]:
                yakus = (YAKU_MAP[fan["id"]] for fan in hule["fans"])
                is_important = False
                for yaku in yakus:
                    # check important yaku
                    if yaku in IMPORTANT_YAKUS:
                        is_important = True
                        seat = 0
                        if "seat" in hule:
                            seat = hule["seat"]
                        for player in player_ranks:
                            if player["seat"] == seat:
                                noted_yakus.append(
                                    {
                                        "yaku": yaku,
                                        "player": player,
                                    }
                                )
                                break
                # check counted yakuman
                if not is_important and hule["count"] >= 13:
                    seat = 0
                    if "seat" in hule:
                        seat = hule["seat"]
                    for player in player_ranks:
                        if player["seat"] == seat:
                            noted_yakus.append(
                                {
                                    "yaku": "헤아림역만",
                                    "player": player,
                                }
                            )
                            break

        return jsonify(
            {
                "result": "OK",
                "uuid": head["uuid"],
                "roomId": head["config"]["meta"]["roomId"],
                "startTime": head["startTime"],
                "endTime": head["endTime"],
                "ranks": player_ranks,
                "noted_yakus": noted_yakus,
            }
        )
    except Exception:
        return (
            jsonify(
                {
                    "result": "ERROR",
                    "message": traceback.format_exc(),
                    "errors": [
                        {
                            "code": "unexpected-exception",
                            "message": "Unexpected exception.",
                        }
                    ],
                    "data": data,
                }
            ),
            500,
        )


@bp.route("/uuid-csv/<uuid>")
async def route_uuid_csv(uuid: str) -> "ResponseReturnValue":
    """Serve simple Majsoul log as csv

    Args:
        uuid (str): uuid of Majsoul log

    Returns:
        ResponseReturnValue: simple Majsoul log as csv
    """
    response = await route_uuid(uuid)
    if isinstance(response, tuple):
        status_code = response[1]
        response = response[0]
    else:
        status_code = response.status_code

    if status_code != 200:
        if status_code == 500:
            result = response.get_json()
            if result["result"] == "ERROR":
                rows = [""] * 10
                rows.append(
                    "Error: ("
                    + ") & (".join(error["message"] for error in result["errors"])
                    + ")"
                )
                return csv_response(rows), status_code
        return response, status_code

    result = response.get_json()
    date = datetime.fromtimestamp(result["startTime"], timezone.utc).astimezone(
        timezone(timedelta(hours=9))
    )
    rows = ["{date.year}년 {date.month}월 {date.day}일".format(date=date)]
    for rank in result["ranks"]:
        rows.append(rank["nickname"])
        rows.append(rank["finalPoint"])
    if result["noted_yakus"]:
        rows.append("")
        rows.append(
            "/".join(
                f'{noted_yaku["player"]["rank"]}위 {noted_yaku["yaku"]}'
                for noted_yaku in result["noted_yakus"]
            )
        )
    return csv_response(rows)
