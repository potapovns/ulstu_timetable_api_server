import os
import logger
import api_timetable
from flask import Flask
from flask_restful import Api
from loguru import logger as log

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_API")

HOST = os.getenv("SERVER_HOST")
PORT = os.getenv("SERVER_PORT")


def main():
    logger.initialize_logger()
    log.info("Logger initialized")

    app.register_blueprint(api_timetable.blueprint)
    log.info("Blueprint registered")
    while True:
        try:
            log.info("Server starting")
            app.run(port=PORT, host=HOST)
        except Exception as e:
            log.exception("")
            log.critical("Server down! Restarting...")


if __name__ == '__main__':
    main()
