import os

from flask import jsonify

import env
from loguru import logger as log

try:
    import credentials
except ImportError:
    log.warning("Credentials file not found! Please set credentials to environ variables.")

import flask
import requests

URL_API = os.getenv("ULSTU_URL_API")
HEADERS_API = {
    "GET": "HTTP/1.1",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

URL_AUTH = os.getenv("ULSTU_URL_AUTH")
HEADERS_AUTH = {
    "POST": "HTTP/1.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "22",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "lk.ulstu.ru",
    "Origin": "https://lk.ulstu.ru",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

USERNAME = None
PASSWORD = None

blueprint = flask.Blueprint(
    'timetable_api',
    __name__,
    template_folder='templates'
)


def initialize_credentials():
    global USERNAME
    global PASSWORD
    USERNAME = os.getenv('ULSTU_USERNAME', None)
    PASSWORD = os.getenv('ULSTU_PASSWORD', None)


def authenticate(session):
    log.debug("Try to authenticate")
    try:
        response = session.post(
            URL_AUTH,
            data={
                "login": USERNAME,
                "password": PASSWORD
            },
            params={
                "q": "auth/login",
                "r": "q=home"
            },
            headers=HEADERS_AUTH
        )
        if not response:
            raise Exception(str(response))
        log.debug("Authenticated done!")
        return response
    except Exception as e:
        log.exception("Authentication error!")


def get_groups_list(session):
    log.debug("Try to get groups")
    try:
        response = session.get(
            URL_API + "groups",
            headers=HEADERS_API
        )
        if not response:
            raise Exception(str(response))
        log.debug("Get groups done!")
        return response.json()
    except Exception as e:
        log.exception("Get groups error!")


def get_timetable_by_groupname(session, groupname):
    log.debug(f"Try to get timetable for group [{groupname}]")
    try:
        response = session.get(
            URL_API + "timetable",
            headers=HEADERS_API,
            params={
                "filter": groupname
            }
        )
        if not response:
            raise Exception(str(response))
        log.debug(f"Get timetable for group [{groupname}] done!")
        return response.json()
    except Exception as e:
        log.exception(f"Get timetable error! Group [{groupname}]")


@blueprint.route('/api/timetable/<string:group_name>', methods=['GET'])
def api_get_timetable_by_group_name(group_name):
    if USERNAME is None or PASSWORD is None:
        initialize_credentials()
    if USERNAME is None or PASSWORD is None:
        return jsonify({"error": "Credentials environment required!"}), 400
    session = requests.Session()
    authenticate(session)
    response_json = get_timetable_by_groupname(session, group_name)
    return response_json, 200


@blueprint.route('/api/timetable/groups', methods=['GET'])
def api_get_groups():
    if USERNAME is None or PASSWORD is None:
        initialize_credentials()
    if USERNAME is None or PASSWORD is None:
        return jsonify({"error": "Credentials environment required!"}), 400
    session = requests.Session()
    authenticate(session)
    response_json = get_groups_list(session)
    return response_json, 200
