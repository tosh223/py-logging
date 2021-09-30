import os
import json
import logging
import time
import traceback

def set_logger():
    level = getattr(logging, os.environ.get('LOG_LEVEL'))
    FMT = '%(asctime)s.%(msecs)03d\t%(filename)s:%(funcName)s:%(lineno)d\t[%(levelname)s]%(message)s'
    DATE_FMT = '%Y-%m-%d %H:%M:%S'
    fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
    fmt.converter = time.gmtime

    root_logger = logging.getLogger()
    print(root_logger.handlers) # [<LambdaLoggerHandler (NOTSET)>]
    root_logger.handlers[0].setLevel(level)
    root_logger.handlers[0].setFormatter(fmt)

def main(event, context):
    logger = logging.getLogger(__name__)
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warn')

    logger.info(event)
    logger.info(context)

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

def lambda_handler(event, context):
    set_logger()
    main(event, context)
