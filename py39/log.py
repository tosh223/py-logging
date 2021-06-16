from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG

logger = getLogger(__name__)
fmt = Formatter('%(asctime)s %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s')

sh = StreamHandler()
sh.setLevel(DEBUG)
sh.setFormatter(fmt)

fh = FileHandler('test.log', 'a+')
fh.setLevel(DEBUG)
fh.setFormatter(fmt)

logger.setLevel(DEBUG)
logger.addHandler(sh)
logger.addHandler(fh)
logger.propagate = False

try:
    logger.info('Info')
    logger.warning('Warn')
    logger.error('Error')
    raise ValueError('ValueError')
except Exception as e:
    logger.exception(e)
