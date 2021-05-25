from flask import Flask, json, jsonify, make_response
import os
from io import StringIO
import hashlib
import hmac
import logging
import random
import uuid
import csv
from datetime import datetime, timedelta, timezone

import aiohttp

from ms.base import MSRPCChannel
from ms.rpc import Lobby
import ms.protocol_pb2 as pb
from google.protobuf.json_format import MessageToJson

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

MS_HOST = "https://game.maj-soul.com"


async def get_log(uuid):
    username = os.environ['MAJSOUL_USERNAME']
    password = os.environ['MAJSOUL_PASSWORD']

    if not username or not password:
        logging.error("Username or password cant be empty")

    lobby, channel = await connect()
    await login(lobby, username, password)

    game_log = await load_and_process_game_log(lobby, uuid)

    await channel.close()
    return game_log


async def connect():
    async with aiohttp.ClientSession() as session:
        async with session.get("{}/1/version.json".format(MS_HOST)) as res:
            version = await res.json()
            logging.info(f"Version: {version}")

            version = version["version"]

        async with session.get("{}/1/v{}/config.json".format(MS_HOST, version)) as res:
            config = await res.json()
            logging.info(f"Config: {config}")

            url = config["ip"][0]["region_urls"][1]["url"]

        async with session.get(url + "?service=ws-gateway&protocol=ws&ssl=true") as res:
            servers = await res.json()
            logging.info(f"Available servers: {servers}")

            servers = servers["servers"]
            server = random.choice(servers)
            endpoint = "wss://{}/".format(server)

    logging.info(f"Chosen endpoint: {endpoint}")
    channel = MSRPCChannel(endpoint)

    lobby = Lobby(channel)

    await channel.connect(MS_HOST)
    logging.info("Connection was established")

    return lobby, channel


async def login(lobby, username, password):
    logging.info("Login with username and password")

    uuid_key = str(uuid.uuid1())

    req = pb.ReqLogin()
    req.account = username
    req.password = hmac.new(b"lailai", password.encode(), hashlib.sha256).hexdigest()
    req.device.is_browser = True
    req.random_key = uuid_key
    req.gen_access_token = True
    req.currency_platforms.append(2)

    res = await lobby.login(req)
    token = res.access_token
    if not token:
        logging.error("Login Error:")
        logging.error(res)
        return False

    return True


async def load_and_process_game_log(lobby, uuid):
    logging.info("Loading game log")
    req = pb.ReqGameRecord()
    req.game_uuid = uuid
    res = await lobby.fetch_game_record(req)
    return res


def print_data_as_json(data, type):
    json = MessageToJson(data)
    logging.info("{} json {}".format(type, json))


app = Flask(__name__)

@app.route("/")
def flask_index():
    return "<p>Hello, World!</p>"

@app.route("/uuid/<uuid>")
async def flask_result(uuid):
    data = MessageToJson(await get_log(uuid))
    data = json.loads(data)
    try:
        head = data['head']

        if 'roomId' not in head['config']['meta']:
            return jsonify({
                'result': 'ERROR',
                'message': "roomId is missing.",
                'data': data
            }), 500

        players = head['accounts']
        results = head['result']['players']
        
        res = []
        for result in results:
            if 'seat' in result:
                seat = result['seat']
                for player in players:
                    if 'seat' in player and player['seat'] == seat:
                        res.append({
                            'id': player['accountId'],
                            'nickname': player['nickname'],
                            'finalPoint': result['partPoint1']
                        })
                        break
            else:
                for player in players:
                    if 'seat' not in player:
                        res.append({
                            'id': player['accountId'],
                            'nickname': player['nickname'],
                            'finalPoint': result['partPoint1']
                        })
                        break
        return jsonify({
            'result': 'OK',
            'uuid': head['uuid'],
            'roomId': head['config']['meta']['roomId'],
            'startTime': head['startTime'],
            'endTime': head['endTime'],
            'ranks': res
        })
    except:
        return jsonify({
            'result': 'ERROR',
            'message': "???",
            'data': data
        }), 500

@app.route("/uuid-csv/<uuid>")
async def flask_result_csv(uuid):
    response = await flask_result(uuid)
    if (isinstance(response, tuple) and response[1] != 200) or response.status_code != 200:
        return response
    result = response.get_json()
    date = datetime.fromtimestamp(result['startTime'], timezone.utc).astimezone(timezone(timedelta(hours=9)))
    si = StringIO()
    cw = csv.writer(si)
    # row = [date.isoformat()]
    row = ['{date.year}년 {date.month}월 {date.day}일'.format(date=date)]
    for rank in result['ranks']:
        row.append(rank['nickname'])
        row.append(rank['finalPoint'])
    cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output