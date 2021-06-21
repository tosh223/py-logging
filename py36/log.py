import sys
import logging
from time import gmtime
from traceback import format_exception_only

from yaml import safe_load

CONFIG_FILE = 'logging.yaml'


class ConfiguredLogger():
    def __init__(self):
        with open(CONFIG_FILE) as file:
            conf = safe_load(file)
        logging.config.dictConfig(conf)
        logging.Formatter.converter = gmtime
    
    def create(self, name):
        return logging.getLogger(name)


class HandmadeLogger():
    def __init__(self, log_level):
        self.__num_level = getattr(logging, log_level)
        default_fmt = logging.Formatter()
        default_fmt.converter = gmtime
        FMT = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
        DATE_FMT = '%Y-%m-%d %H:%M:%S'
        verbose_fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
        verbose_fmt.converter = gmtime

        self.__sh = logging.StreamHandler()
        self.__sh.setLevel(self.__num_level)
        self.__sh.setFormatter(default_fmt)

        self.__fh = logging.FileHandler('test.log', 'a+')
        self.__fh.setLevel(self.__num_level)
        self.__fh.setFormatter(verbose_fmt)

    def create(self, name):
        my_logger = logging.getLogger(name)
        my_logger.setLevel(self.__num_level)
        my_logger.addHandler(self.__sh)
        my_logger.addHandler(self.__fh)
        my_logger.propagate = False
        return my_logger


def main(log_level='WARN'):
    try:
        # my_logger = ConfiguredLogger().create(__name__)
        my_logger = HandmadeLogger(log_level).create(__name__)
        my_logger.debug('Debug')
        my_logger.info('Info')
        my_logger.warning('Warn')
        my_logger.error('Error')
        my_logger.critical('Critical')
        raise ValueError('Error test')

    except Exception as e:
        ### Error message only
        my_logger.error(e)
        my_logger.exception(e, exc_info=False)

        ### With stacktrace
        my_logger.error(e, exc_info=True)
        my_logger.exception(e)

        ### Without stacktrace
        my_logger.error('{}: {}'.format(str(e.__class__.__name__), str(e)))
        my_logger.error(format_exception_only(type(e), e)[0].rstrip('\n'))


if __name__ == '__main__':
    log_level = 'WARN'
    if len(sys.argv) > 1:
        log_level = sys.argv[1]
    main(log_level)
