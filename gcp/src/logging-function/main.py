import os
import json
from logging import Formatter, getLevelName, getLogger
import traceback

### For using default settings
# from google.cloud.logging import Client
# client = Client()
# client.setup_logging()      # [<StructuredLogHandler <stderr> (NOTSET)>]

### For custom settings
from google.cloud.logging.handlers import StructuredLogHandler, setup_logging

FMT = '%(asctime)s.%(msecs)03d\t%(filename)s:%(funcName)s:%(lineno)d\t[%(levelname)s]%(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'
fmt = Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
level = getLevelName(os.environ.get('LOG_LEVEL'))
handler = StructuredLogHandler()
handler.setLevel(level)
handler.setFormatter(fmt)
setup_logging(handler, log_level=level)

def handler(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    logger = getLogger(__name__)
    logger.debug('Debug')
    logger.info(f'Info {request_json}')
    logger.warning('Warn')
    logger.error('Error')
    logger.critical('Critical')

    try:
        raise ValueError('Error test')

    except Exception as e:
        traceback_str = traceback.format_exc().splitlines()
        err_msg = json.dumps({
            "errorType": e.__class__.__name__,
            "errorMessage": e.__str__(),
            "stackTrace": traceback_str
        })
        logger.error(err_msg)
        return err_msg
