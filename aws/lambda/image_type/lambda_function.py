import os
import json
import logging
import time
import traceback

level = logging.getLevelName(os.environ.get('LOG_LEVEL'))
FMT = '%(asctime)s.%(msecs)03d\t%(aws_request_id)s\t%(filename)s:%(funcName)s:%(lineno)d\t[%(levelname)s]%(message)s\n'
DATE_FMT = '%Y-%m-%d %H:%M:%S'
fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
fmt.converter = time.gmtime

root_logger = logging.getLogger()
root_logger.setLevel(level)
root_logger.handlers[0].setLevel(level)
root_logger.handlers[0].setFormatter(fmt)

def main(event, context):
    logger = logging.getLogger(__name__)
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warn')

    logger.info(event)
    logger.info(vars(context))

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
    main(event, context)
