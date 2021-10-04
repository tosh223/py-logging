import sys
import logging

from awsglue.utils import getResolvedOptions

print(logging.getLogger().handlers) # [<StreamHandler <stderr> (NOTSET)>]

args = getResolvedOptions(sys.argv, ['log_level'])
level = logging.getLevelName(args['log_level'])

logger = logging.getLogger(__name__)
logger.setLevel(level)

logger.debug('Debug')
logger.info('Info')
logger.warning('Warn')
logger.error('Error')
logger.critical('Critical')
raise ValueError('Error test')
