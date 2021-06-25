import sys
import logging

from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['log_level'])

print(logging.getLogger().handlers) # [<StreamHandler <stderr> (NOTSET)>]

level = getattr(logging, args['log_level'])
FMT = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'
fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')

sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(level)
sh.setFormatter(fmt)

logger = logging.getLogger()
[logger.removeHandler(h) for h in logger.handlers]

logger = logging.getLogger(__name__)
logger.setLevel(level)
logger.addHandler(sh)
logger.propagate = False

logger.debug('Debug')
logger.info('Info')
logger.warning('Warn')
logger.error('Error')
logger.critical('Critical')
raise ValueError('Error test')
