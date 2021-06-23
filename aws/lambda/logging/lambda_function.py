import os
import sys
import json
import logging
import traceback

LOG_LEVEL = os.environ.get('LOG_LEVEL')
level = getattr(logging, LOG_LEVEL)
FMT = '%(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
fmt = logging.Formatter(fmt=FMT, style='%')

sh = logging.StreamHandler()
sh.setLevel(level)
sh.setFormatter(fmt)

logger = logging.getLogger(__name__)
logger.setLevel(level)
logger.addHandler(sh)
logger.propagate = False

def main(event, context):
    try:
        logger.debug('Debug')
        logger.info('Info')
        logger.warning('Warn')

        logger.info(event)
        logger.info(context)

        logger.error('Error')
        logger.critical('Critical')
        raise ValueError('Error test')

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        err_msg = json.dumps({
            "errorType": exc_type.__name__,
            "errorMessage": str(exc_value),
            "stackTrace": traceback_str
        })
        logger.error(err_msg)

def lambda_handler(event, context):
    main(event, context)
