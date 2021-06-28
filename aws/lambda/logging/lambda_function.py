import os
import json
import logging
import traceback

level = getattr(logging, os.environ.get('LOG_LEVEL'))
FMT = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'
fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')

sh = logging.StreamHandler()
sh.setLevel(level)
sh.setFormatter(fmt)

print(logging.getLogger().handlers) # [<LambdaLoggerHandler (NOTSET)>]
logger = logging.getLogger()
[logger.removeHandler(h) for h in logger.handlers]

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
        traceback_str = traceback.format_exc().splitlines()
        err_msg = json.dumps({
            "errorType": e.__class__.__name__,
            "errorMessage": e.__str__(),
            "stackTrace": traceback_str
        })
        logger.error(err_msg)

def lambda_handler(event, context):
    main(event, context)
