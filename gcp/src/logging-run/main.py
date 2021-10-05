import os
import json
from logging import Formatter, getLevelName
import traceback

from flask import Flask, abort
from werkzeug.exceptions import InternalServerError
from google.cloud.logging.handlers import StructuredLogHandler, setup_logging

app = Flask(__name__)

FMT = '%(asctime)s.%(msecs)03d\t%(filename)s:%(funcName)s:%(lineno)d\t[%(levelname)s]%(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'
fmt = Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
level = getLevelName(os.environ.get('LOG_LEVEL'))
handler = StructuredLogHandler()
handler.setLevel(level)
handler.setFormatter(fmt)
setup_logging(handler, log_level=level)

@app.errorhandler(InternalServerError)
def error_handler(e):
    return 'InternalServerError has occured.', e.code

@app.route("/")
def test_logging():
    app.logger.debug('Debug')
    app.logger.info('Info')
    app.logger.warning('Warn')
    app.logger.error('Error')
    app.logger.critical('Critical')

    try:
        raise InternalServerError('Error test')

    except Exception as e:
        traceback_str = traceback.format_exc().splitlines()
        err_msg = json.dumps({
            "errorType": e.__class__.__name__,
            "errorMessage": e.__str__(),
            "stackTrace": traceback_str
        })
        app.logger.error(err_msg)
        abort(e.code)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
