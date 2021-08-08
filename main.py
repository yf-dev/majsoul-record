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
import traceback

import aiohttp

from ms.base import MSRPCChannel
from ms.rpc import Lobby
import ms.protocol_pb2 as pb
from google.protobuf.json_format import MessageToJson

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

MS_HOST = os.environ['MAJSOUL_HOST']
CLIENT_VERSION_STRING = os.environ['MAJSOUL_CLIENT_VERSION']

YAKU = {
    1: '멘젠쯔모',
    2: '리치',
    3: '창깡',
    4: '영상개화',
    5: '해저로월',
    6: '하저로어',
    7: '역패: 백',
    8: '역패: 발',
    9: '역패: 중',
    10: '자풍패',
    11: '장풍패',
    12: '탕야오',
    13: '이페코',
    14: '핑후',
    15: '찬타',
    16: '일기통관',
    17: '삼색동순',
    18: '더블리치',
    19: '삼색동각',
    20: '산깡즈',
    21: '또이또이',
    22: '산안커',
    23: '소삼원',
    24: '혼노두',
    25: '치또이츠',
    26: '준찬타',
    27: '혼일색',
    28: '량페코',
    29: '청일색',
    30: '일발',
    31: '도라',
    32: '적도라',
    33: '뒷도라',
    34: '북도라',
    35: '천화',
    36: '지화',
    37: '대삼원',
    38: '스안커',
    39: '자일색',
    40: '녹일색',
    41: '청노두',
    42: '국사무쌍',
    43: '소사희',
    44: '스깡즈',
    45: '구련보등',
    46: '팔연장',
    47: '순정구련보등',
    48: '스안커 단기',
    49: '국사무쌍 13면대기',
    50: '대사희',
    51: '츠바메가에시',
    52: '영상개론',
    53: '십이낙태',
    54: '오문제',
    55: '삼련각',
    56: '일색삼순',
    57: '일통모월',
    58: '구통로어',
    59: '인화',
    60: '대차륜',
    61: '대죽림',
    62: '대수린',
    63: '돌 위에서 삼년',
    64: '대칠성',
}

IMPORTANT_YAKUS = [
    '천화',
    '지화',
    '대삼원',
    '스안커',
    '자일색',
    '녹일색',
    '청노두',
    '국사무쌍',
    '소사희',
    '스깡즈',
    '구련보등',
    '팔연장',
    '순정구련보등',
    '스안커 단기',
    '국사무쌍 13면대기',
    '대사희',
    '츠바메가에시',
    '영상개론',
    '십이낙태',
    '오문제',
    '삼련각',
    '일색삼순',
    '일통모월',
    '구통로어',
    '인화',
    '대차륜',
    '대죽림',
    '대수린',
    '돌 위에서 삼년',
    '대칠성',
]


async def get_log(uuid):
    username = os.environ['MAJSOUL_USERNAME']
    password = os.environ['MAJSOUL_PASSWORD']

    if not username or not password:
        logging.error("Username or password cant be empty")

    lobby, channel = await connect()
    await login(lobby, username, password)
    
    game_log, records = await load_and_process_game_log(lobby, uuid)

    await channel.close()
    return game_log, records


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
    req.client_version_string = CLIENT_VERSION_STRING
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
    req.client_version_string = CLIENT_VERSION_STRING
    res = await lobby.fetch_game_record(req)

    record_wrapper = pb.Wrapper()
    record_wrapper.ParseFromString(res.data)

    game_details = pb.GameDetailRecords()
    game_details.ParseFromString(record_wrapper.data)

    records = []

    record_actions = (action for action in game_details.actions if hasattr(action, 'result') and len(action.result) > 0)
    for record_action in record_actions:
        round_record_wrapper = pb.Wrapper()
        round_record_wrapper.ParseFromString(record_action.result)
        round_record_classname = round_record_wrapper.name[4:]
        if round_record_classname in ['RecordHule']:
            round_record_class = getattr(pb, round_record_classname)
            round_record = round_record_class()
            round_record.ParseFromString(round_record_wrapper.data)
            records.append({
                'name': round_record_classname,
                'data': json.loads(MessageToJson(round_record))
            })

    return res, records


def print_data_as_json(data, type):
    json = MessageToJson(data)
    logging.info("{} json {}".format(type, json))


app = Flask(__name__)

@app.route("/uuid-raw/<uuid>")
async def flask_result_test(uuid):
    game_log, records = await get_log(uuid)
    data = MessageToJson(game_log)
    data = json.loads(data)
    data['records'] = records
    del data['data']
    return jsonify(data)

@app.route("/uuid/<uuid>")
async def flask_result(uuid):
    game_log, records = await get_log(uuid)
    data = MessageToJson(game_log)
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
                            'seat': seat,
                            'nickname': player['nickname'],
                            'finalPoint': result['partPoint1']
                        })
                        break
            else:
                for player in players:
                    if 'seat' not in player:
                        res.append({
                            'id': player['accountId'],
                            'seat': 0,
                            'nickname': player['nickname'],
                            'finalPoint': result['partPoint1']
                        })
                        break

        res.sort(key=lambda player: player['finalPoint'], reverse=True)
        for i in range(len(res)):
            res[i]['rank'] = i + 1
        
        noted_yakus = []
        for record in records:
            if record['name'] != 'RecordHule':
                continue
            for hule in record['data']['hules']:
                yakus = (YAKU[fan['id']] for fan in hule['fans'])
                is_important = False
                for yaku in yakus:
                    if yaku in IMPORTANT_YAKUS:
                        is_important = True
                        seat = 0
                        if 'seat' in hule:
                            seat = hule['seat']
                        for player in res:
                            if player['seat'] == seat:
                                noted_yakus.append({
                                    'yaku': yaku,
                                    'player': player,
                                })
                                break
                if not is_important and hule['count'] >= 13:
                    seat = 0
                    if 'seat' in hule:
                        seat = hule['seat']
                    for player in res:
                        if player['seat'] == seat:
                            noted_yakus.append({
                                'yaku': '헤아림역만',
                                'player': player,
                            })
                            break

        return jsonify({
            'result': 'OK',
            'uuid': head['uuid'],
            'roomId': head['config']['meta']['roomId'],
            'startTime': head['startTime'],
            'endTime': head['endTime'],
            'ranks': res,
            'noted_yakus': noted_yakus
        })
    except Exception as e:
        data['records'] = records
        del data['data']
        return jsonify({
            'result': 'ERROR',
            'message': traceback.format_exc(),
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
    if result['noted_yakus']:
        row.append('')
        row.append('/'.join(f'{noted_yaku["player"]["rank"]}위 {noted_yaku["yaku"]}' for noted_yaku in result['noted_yakus']))
    cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output