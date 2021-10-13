from typing import List
from flask.testing import FlaskClient
import pytest

from src import create_app


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        yield client


def test_uuid_1(client: FlaskClient):
    rv = client.get("/uuid/210525-e9e55c55-f25c-497c-a435-7e29a6df2483")
    json_data = rv.get_json()
    expected_data = {
        "endTime": 1621938770,
        "noted_yakus": [],
        "ranks": [
            {
                "finalPoint": 36400,
                "id": 75260973,
                "nickname": "sniper131",
                "rank": 1,
                "seat": 2,
            },
            {
                "finalPoint": 30600,
                "id": 67412632,
                "nickname": "memoru",
                "rank": 2,
                "seat": 1,
            },
            {
                "finalPoint": 29100,
                "id": 69560545,
                "nickname": "SiraB",
                "rank": 3,
                "seat": 0,
            },
            {
                "finalPoint": 3900,
                "id": 72081250,
                "nickname": "Pain",
                "rank": 4,
                "seat": 3,
            },
        ],
        "result": "OK",
        "roomId": 20496,
        "startTime": 1621937111,
        "uuid": "210525-e9e55c55-f25c-497c-a435-7e29a6df2483",
    }
    assert json_data is not None
    assert json_data.items() == expected_data.items()


def test_uuid_2(client: FlaskClient):
    rv = client.get("/uuid/210525-e6db23af-23ee-446a-b746-48cf02f4028c")
    json_data = rv.get_json()
    expected_data = {
        "endTime": 1621936938,
        "noted_yakus": [],
        "ranks": [
            {
                "finalPoint": 33100,
                "id": 75260973,
                "nickname": "sniper131",
                "rank": 1,
                "seat": 3,
            },
            {
                "finalPoint": 25800,
                "id": 121523715,
                "nickname": "Rabi_Arna",
                "rank": 2,
                "seat": 2,
            },
            {
                "finalPoint": 24800,
                "id": 69560545,
                "nickname": "SiraB",
                "rank": 3,
                "seat": 0,
            },
            {
                "finalPoint": 16300,
                "id": 72022595,
                "nickname": "Pororoka",
                "rank": 4,
                "seat": 1,
            },
        ],
        "result": "OK",
        "roomId": 70001,
        "startTime": 1621935312,
        "uuid": "210525-e6db23af-23ee-446a-b746-48cf02f4028c",
    }
    assert json_data is not None
    assert json_data.items() == expected_data.items()


def test_uuid_3(client: FlaskClient):
    rv = client.get("/uuid/210920-74d53b38-bcf7-4b62-870a-5da587bf4f51")
    json_data = rv.get_json()
    expected_data = {
        "endTime": 1632144420,
        "noted_yakus": [],
        "ranks": [
            {
                "finalPoint": 40500,
                "id": 75273220,
                "nickname": "天使",
                "rank": 1,
                "seat": 2,
            },
            {
                "finalPoint": 36800,
                "id": 72543579,
                "nickname": "c909",
                "rank": 2,
                "seat": 3,
            },
            {
                "finalPoint": 33700,
                "id": 120130724,
                "nickname": "UNIS",
                "rank": 3,
                "seat": 1,
            },
            {
                "finalPoint": -11000,
                "id": 70539505,
                "nickname": "Kailua",
                "rank": 4,
                "seat": 0,
            },
        ],
        "result": "OK",
        "roomId": 79734,
        "startTime": 1632142202,
        "uuid": "210920-74d53b38-bcf7-4b62-870a-5da587bf4f51",
    }
    assert json_data is not None
    assert json_data.items() == expected_data.items()


def test_uuid_4(client: FlaskClient):
    rv = client.get("/uuid/211006-1701b755-1439-460a-8c5d-28aedbcc8651")
    json_data = rv.get_json()
    expected_data = {
        "endTime": 1633525844,
        "noted_yakus": [],
        "ranks": [
            {
                "finalPoint": 77000,
                "id": 118305315,
                "nickname": "Boob",
                "rank": 1,
                "seat": 3,
            },
            {
                "finalPoint": 11800,
                "id": 121540433,
                "nickname": "HiPerf_Roh",
                "rank": 2,
                "seat": 2,
            },
            {
                "finalPoint": 11200,
                "id": 75273220,
                "nickname": "天使",
                "rank": 3,
                "seat": 1,
            },
            {
                "finalPoint": 0,
                "id": 74492104,
                "nickname": "Helith",
                "rank": 4,
                "seat": 0,
            },
        ],
        "result": "OK",
        "roomId": 16509,
        "startTime": 1633523610,
        "uuid": "211006-1701b755-1439-460a-8c5d-28aedbcc8651",
    }
    assert json_data is not None
    assert json_data.items() == expected_data.items()


def test_uuid_noted_yakus(client: FlaskClient):
    rv = client.get("/uuid/210807-3a956b38-1df3-48db-b06e-9f1b0a28ba48")
    json_data = rv.get_json()
    expected_data = {
        "endTime": 1628302475,
        "noted_yakus": [
            {
                "player": {
                    "finalPoint": 49300,
                    "id": 75134334,
                    "nickname": "AI123123123",
                    "rank": 1,
                    "seat": 2,
                },
                "yaku": "국사무쌍",
            }
        ],
        "ranks": [
            {
                "finalPoint": 49300,
                "id": 75134334,
                "nickname": "AI123123123",
                "rank": 1,
                "seat": 2,
            },
            {
                "finalPoint": 33600,
                "id": 67906613,
                "nickname": "ice_Mocha",
                "rank": 2,
                "seat": 3,
            },
            {
                "finalPoint": 30300,
                "id": 74030349,
                "nickname": "BlackSeed",
                "rank": 3,
                "seat": 1,
            },
            {
                "finalPoint": -13200,
                "id": 124782781,
                "nickname": "MightyMoon",
                "rank": 4,
                "seat": 0,
            },
        ],
        "result": "OK",
        "roomId": 20481,
        "startTime": 1628300996,
        "uuid": "210807-3a956b38-1df3-48db-b06e-9f1b0a28ba48",
    }
    assert json_data is not None
    assert json_data.items() == expected_data.items()


def test_uuid_error_invalid_uuid(client: FlaskClient):
    rv = client.get("/uuid/invalid-uuid")
    json_data = rv.get_json()
    expected_errors = [
        {
            "code": "cannot-get-log",
            "data": None,
            "message": "Cannot get game log data.",
        }
    ]
    assert json_data is not None
    assert json_data["result"] == "ERROR"
    assert json_data["errors"] == expected_errors


def test_uuid_error_rank_match(client: FlaskClient):
    rv = client.get("/uuid/210924-e9b30815-f8ec-4f46-a174-819e9b64512a")
    json_data = rv.get_json()
    expected_errors = [
        {"code": "missing-room-id", "data": None, "message": "roomId is missing."}
    ]
    assert json_data is not None
    assert json_data["result"] == "ERROR"
    assert json_data["errors"] == expected_errors


def test_uuid_error_3_player(client: FlaskClient):
    rv = client.get("/uuid/210903-b2002166-5daf-4c35-b053-c185f680a559")
    json_data = rv.get_json()
    expected_errors = [
        {
            "code": "invalid-player-count",
            "data": 3,
            "message": "Invalid player count: 3. It should be 4.",
        },
        {
            "code": "invalid-mode",
            "data": 12,
            "message": "Invalid mode: 12. It should be 4-Player Two-Wind Match Mode(2).",
        },
        {
            "code": "invalid-red-dora",
            "data": 2,
            "message": "Invalid red dora: 2. It should be 3.",
        },
        {
            "code": "invalid-min-points-to-win",
            "data": 40000,
            "message": "Invalid min points to win: 40000. It should be 30000.",
        },
        {
            "code": "invalid-starting-points",
            "data": 35000,
            "message": "Invalid starting points: 35000. It should be 25000.",
        },
    ]
    assert json_data is not None
    assert json_data["result"] == "ERROR"
    assert json_data["errors"] == expected_errors


def test_uuid_error_complex(client: FlaskClient):
    rv = client.get("/uuid/210926-abcf14f9-1d3e-4e3b-8ec2-74731a0d01da")
    json_data = rv.get_json()
    expected_errors = [
        {
            "code": "invalid-player-count",
            "data": 1,
            "message": "Invalid player count: 1. It should be 4.",
        },
        {
            "code": "invalid-mode",
            "data": 1,
            "message": "Invalid mode: 1. It should be 4-Player Two-Wind Match Mode(2).",
        },
        {
            "code": "invalid-red-dora",
            "data": 4,
            "message": "Invalid red dora: 4. It should be 3.",
        },
        {
            "code": "invalid-min-points-to-win",
            "data": 25000,
            "message": "Invalid min points to win: 25000. It should be 30000.",
        },
        {
            "code": "invalid-min-han",
            "data": 2,
            "message": "Invalid min han: 2. It should be 1.",
        },
        {
            "code": "invalid-starting-points",
            "data": 10000,
            "message": "Invalid starting points: 10000. It should be 25000.",
        },
        {
            "code": "invalid-local-yaku",
            "data": 1,
            "message": "Invalid local yaku: 1. It should be 0.",
        },
        {
            "code": "invalid-open-hand",
            "data": 1,
            "message": "Invalid open hand: 1. It should be 0.",
        },
        {
            "code": "invalid-thinking-time-add",
            "data": 5,
            "message": "Invalid thinking time(add): 5. It should be 20.",
        },
        {
            "code": "invalid-thinking-time-fixed",
            "data": 3,
            "message": "Invalid thinking time(fixed): 3. It should be 5.",
        },
    ]
    assert json_data is not None
    assert json_data["result"] == "ERROR"
    assert json_data["errors"] == expected_errors


def test_uuid_raw(client: FlaskClient):
    rv = client.get("/uuid-raw/210525-e9e55c55-f25c-497c-a435-7e29a6df2483")
    json_data = rv.get_json()
    expected_head = {
        "accounts": [
            {
                "accountId": 69560545,
                "avatarId": 400102,
                "character": {
                    "charid": 200001,
                    "extraEmoji": [10, 11, 12],
                    "isUpgraded": True,
                    "level": 5,
                    "skin": 400102,
                },
                "level": {"id": 10303, "score": 994},
                "level3": {"id": 20401, "score": 1047},
                "nickname": "SiraB",
                "views": [{"itemId": 308005, "slot": 7}],
            },
            {
                "accountId": 67412632,
                "avatarId": 404101,
                "character": {
                    "charid": 200041,
                    "exp": 24796,
                    "level": 4,
                    "skin": 404101,
                },
                "level": {"id": 10201, "score": 147},
                "level3": {"id": 20102},
                "nickname": "memoru",
                "seat": 1,
                "title": 600010,
                "views": [
                    {"itemId": 305002},
                    {"itemId": 305039, "slot": 1},
                    {"itemId": 305022, "slot": 2},
                    {"itemId": 305031, "slot": 3},
                    {"itemId": 305026, "slot": 4},
                    {"itemId": 308009, "slot": 6},
                    {"itemId": 308010, "slot": 7},
                ],
            },
            {
                "accountId": 75260973,
                "avatarId": 400101,
                "character": {"charid": 200001, "skin": 400101},
                "level": {"id": 10102},
                "level3": {"id": 20101},
                "nickname": "sniper131",
                "seat": 2,
            },
            {
                "accountId": 72081250,
                "avatarId": 400901,
                "character": {
                    "charid": 200009,
                    "extraEmoji": [10, 11, 12, 994],
                    "isUpgraded": True,
                    "level": 5,
                    "skin": 400901,
                },
                "level": {"id": 10403, "score": 787},
                "level3": {"id": 20402, "score": 1294},
                "nickname": "Pain",
                "seat": 3,
                "views": [
                    {"itemId": 305019},
                    {"itemId": 308006, "slot": 1},
                    {"itemId": 308007, "slot": 2},
                    {"itemId": 305901, "slot": 10},
                    {"itemId": 305031, "slot": 3},
                    {"itemId": 305026, "slot": 4},
                    {"itemId": 308009, "slot": 6},
                    {"itemId": 308010, "slot": 7},
                    {"itemId": 307006, "slot": 8},
                ],
            },
        ],
        "config": {
            "category": 1,
            "meta": {"roomId": 20496},
            "mode": {
                "ai": True,
                "detailRule": {
                    "aiLevel": 1,
                    "bianjietishi": True,
                    "doraCount": 3,
                    "fandian": 30000,
                    "fanfu": 1,
                    "initPoint": 25000,
                    "shiduan": 1,
                    "timeAdd": 20,
                    "timeFixed": 5,
                },
                "mode": 2,
            },
        },
        "endTime": 1621938770,
        "result": {
            "players": [
                {"partPoint1": 36400, "seat": 2, "totalPoint": 26400},
                {"partPoint1": 30600, "seat": 1, "totalPoint": 10600},
                {"partPoint1": 29100, "totalPoint": -900},
                {"partPoint1": 3900, "seat": 3, "totalPoint": -36100},
            ]
        },
        "startTime": 1621937111,
        "uuid": "210525-e9e55c55-f25c-497c-a435-7e29a6df2483",
    }
    assert json_data is not None
    assert json_data["head"].items() == expected_head.items()
    assert type(json_data["records"]) is list


def test_uuid_raw_error(client: FlaskClient):
    rv = client.get("/uuid-raw/invalid-uuid")
    json_data = rv.get_json()
    assert json_data is not None
    assert "error" in json_data


def test_uuid_csv(client: FlaskClient):
    rv = client.get("/uuid-csv/210525-e9e55c55-f25c-497c-a435-7e29a6df2483")
    csv_data = rv.data.decode("utf-8")
    expected_data = (
        "2021년 5월 25일,sniper131,36400,memoru,30600,SiraB,29100,Pain,3900,20496\r\n"
    )
    assert csv_data == expected_data


def test_uuid_csv_noted_yakus(client: FlaskClient):
    rv = client.get("/uuid-csv/210807-3a956b38-1df3-48db-b06e-9f1b0a28ba48")
    csv_data = rv.data.decode("utf-8")
    expected_data = "2021년 8월 7일,AI123123123,49300,ice_Mocha,33600,BlackSeed,30300,MightyMoon,-13200,20481,1위 국사무쌍\r\n"
    assert csv_data == expected_data


def test_uuid_error(client: FlaskClient):
    rv = client.get("/uuid-csv/210926-abcf14f9-1d3e-4e3b-8ec2-74731a0d01da")
    csv_data = rv.data.decode("utf-8")
    expected_data = ",,,,,,,,,,Error: (Invalid player count: 1. It should be 4.) & (Invalid mode: 1. It should be 4-Player Two-Wind Match Mode(2).) & (Invalid red dora: 4. It should be 3.) & (Invalid min points to win: 25000. It should be 30000.) & (Invalid min han: 2. It should be 1.) & (Invalid starting points: 10000. It should be 25000.) & (Invalid local yaku: 1. It should be 0.) & (Invalid open hand: 1. It should be 0.) & (Invalid thinking time(add): 5. It should be 20.) & (Invalid thinking time(fixed): 3. It should be 5.)\r\n"
    assert csv_data == expected_data
