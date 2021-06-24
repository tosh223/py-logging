import sys
import logging

from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['log_level'])

level = getattr(logging, args['log_level'])
FMT = '%(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
fmt = logging.Formatter(fmt=FMT, style='%')

sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(level)
sh.setFormatter(fmt)

logger = logging.getLogger()
[logger.removeHandler(h) for h in logger.handlers]

logger = logging.getLogger(__name__)
logger.setLevel(level)
logger.addHandler(sh)
logger.propagate = False

try:
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warn')
    logger.error('Error')
    logger.critical('Critical')
    raise ValueError('Error test')

except Exception as e:
    logger.exception(e)
    exit(e) 
