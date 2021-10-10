import sys
import json
import logging
import traceback

from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['log_level'])
level = logging.getLevelName(args['log_level'])
FMT = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'
fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')

sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(level)
sh.setFormatter(fmt)

root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.setLevel(level)
root_logger.addHandler(sh)

#############################################
logger = logging.getLogger(__name__)
logger.debug('Debug')
logger.info('Info')
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
    exit(1)
