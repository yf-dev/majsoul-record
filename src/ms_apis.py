import os
import json
import hashlib
import hmac
import logging
import random
import uuid
import aiohttp
import typing as t

from ms.base import MSRPCChannel
from ms.rpc import Lobby
import ms.protocol_pb2 as pb
from google.protobuf.json_format import MessageToJson

MS_HOST = os.environ["MAJSOUL_HOST"]


async def connect() -> t.Tuple[Lobby, MSRPCChannel, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("{}/1/version.json".format(MS_HOST)) as res:
            version = await res.json()
            logging.info(f"Version: {version}")

            version = version["version"]
            client_version = "web-" + version.replace(".w", "")

        async with session.get("{}/1/v{}/config.json".format(MS_HOST, version)) as res:
            config = await res.json()
            logging.info(f"Config: {config}")

            url = config["ip"][0]["region_urls"][1]["url"]

        async with session.get(url + "?service=ws-gateway&protocol=ws&ssl=true") as res:
            servers = await res.json()
            logging.info(f"Available servers: {servers}")

            servers = servers["servers"]
            server = random.choice(servers)
            endpoint = "wss://{}/gateway".format(server)

    logging.info(f"Chosen endpoint: {endpoint}")
    channel = MSRPCChannel(endpoint)

    lobby = Lobby(channel)

    await channel.connect(MS_HOST)
    logging.info("Connection was established")

    return lobby, channel, client_version


async def login(
    lobby: Lobby, username: str, password: str, client_version: str
) -> bool:
    logging.info("Login with username and password")

    uuid_key = str(uuid.uuid1())

    req = pb.ReqLogin()
    req.account = username
    req.password = hmac.new(b"lailai", password.encode(), hashlib.sha256).hexdigest()
    req.device.is_browser = True
    req.random_key = uuid_key
    req.gen_access_token = True
    req.client_version_string = client_version
    req.currency_platforms.append(2)

    res = await lobby.login(req)
    token = res.access_token
    if not token:
        logging.error("Login Error:")
        logging.error(res)
        return False

    return True


async def load_and_process_game_log(
    lobby: Lobby, uuid: str, client_version: str
) -> t.Tuple[t.Any, t.List[t.Dict]]:
    logging.info("Loading game log")
    req = pb.ReqGameRecord()
    req.game_uuid = uuid
    req.client_version_string = client_version
    res = await lobby.fetch_game_record(req)

    record_wrapper = pb.Wrapper()
    record_wrapper.ParseFromString(res.data)

    game_details = pb.GameDetailRecords()
    game_details.ParseFromString(record_wrapper.data)

    records = []

    if len(game_details.records) > 0:
        # old format
        record_items = game_details.records
    else:
        # new format
        record_items = (
            action.result
            for action in game_details.actions
            if hasattr(action, "result") and len(action.result) > 0
        )

    for item in record_items:
        round_record_wrapper = pb.Wrapper()
        round_record_wrapper.ParseFromString(item)
        round_record_classname = round_record_wrapper.name[4:]
        round_record_class = getattr(pb, round_record_classname)
        round_record = round_record_class()
        round_record.ParseFromString(round_record_wrapper.data)
        records.append(
            {
                "name": round_record_classname,
                "data": json.loads(MessageToJson(round_record)),
            }
        )

    return res, records


async def get_log(uuid: str) -> t.Dict:
    username = os.environ["MAJSOUL_USERNAME"]
    password = os.environ["MAJSOUL_PASSWORD"]

    if not username or not password:
        logging.error("Username or password cant be empty")

    lobby, channel, client_version = await connect()

    await login(lobby, username, password, client_version)

    game_log, records = await load_and_process_game_log(lobby, uuid, client_version)

    await channel.close()

    data = json.loads(MessageToJson(game_log))  # type: t.Dict[str, t.Any]
    if "data" in data:
        del data["data"]

    if "error" not in data:
        data["records"] = records

    return data
