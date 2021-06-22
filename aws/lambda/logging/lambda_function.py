import os
import logging
from time import gmtime

LOG_LEVEL = os.environ.get('LOG_LEVEL')

class Logger():
    def __init__(self):
        FMT = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
        DATE_FMT = '%Y-%m-%d %H:%M:%S'
        verbose_fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
        verbose_fmt.converter = gmtime

        self.__num_level = getattr(logging, LOG_LEVEL)
        self.__sh = logging.StreamHandler()
        self.__sh.setLevel(self.__num_level)
        self.__sh.setFormatter(verbose_fmt)

    def create(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(self.__num_level)
        logger.addHandler(self.__sh)
        logger.addHandler(self.__fh)
        logger.propagate = False


def main(event, context):
    try:
        logger = Logger().create(__name__)
        logger.debug('Debug')
        logger.info('Info')
        logger.warning('Warn')

        logger.info(event)
        logger.info(context)

        logger.error('Error')
        logger.critical('Critical')
        raise ValueError('Error test')

    except Exception as e:
        logger.error('{}: {}'.format(str(e.__class__.__name__), str(e)))

def lambda_handler(event, context):
    main(event, context)
