import os
import argparse
from time import gmtime
from logging import config, Filter, getLogger, Formatter, StreamHandler, FileHandler, DEBUG, WARN
from traceback import format_exception_only

from yaml import safe_load

class MyLoggingFilter(Filter):
    def __init__(self, level=None):
        self.__target_levelno = self.__get_levelno(level)

    def filter(self, record):
        if record.levelno >= self.__target_levelno:
            return self.__check_message(record.getMessage())
        else:
            return False

    @staticmethod
    def __get_levelno(level_name):
        levelno_dict = {
            'DEBUG': 10,
            'INFO': 20,
            'WARN': 30,
            'ERROR': 40,
            'CRITICAL': 50,
        }
        return levelno_dict.get(level_name, 0)

    @staticmethod
    def __check_message(message):
        return not message.startswith('Credentials')

class ConfiguredLogger():
    def __init__(self, config_file=None):
        current_dir = os.path.dirname(__file__)
        with open(current_dir + '/' + config_file) as file:
            _, ext = os.path.splitext(config_file)
            if ext in ['.yaml', '.yml']:
                conf = safe_load(file)
                config.dictConfig(conf)
            elif ext == '.conf':
                config.fileConfig(file)
            elif ext == '.json':
                pass
            else:
                pass

        Formatter.converter = gmtime
    
    def create(self, name):
        return getLogger(name)


class HandmadeLogger():
    def __init__(self):
        default_fmt = Formatter()
        default_fmt.converter = gmtime
        FMT = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
        DATE_FMT = '%Y-%m-%d %H:%M:%S'
        verbose_fmt = Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
        verbose_fmt.converter = gmtime

        self.__sh = StreamHandler()
        self.__sh.setLevel(WARN)
        self.__sh.setFormatter(default_fmt)

        self.__fh = FileHandler('test.log', 'a+')
        self.__fh.setLevel(DEBUG)
        self.__fh.setFormatter(verbose_fmt)

    def create(self, name):
        logger = getLogger(name)
        logger.setLevel(DEBUG)
        logger.addHandler(self.__sh)
        logger.addHandler(self.__fh)
        logger.addFilter(MyLoggingFilter())
        logger.propagate = False
        return logger


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config", help="logger config file", type=str, default=None
    )

    return parser.parse_args()


def main():
    config_file = get_args().config
    if config_file:
        logger_factory = ConfiguredLogger(config_file=config_file)
    else:
        logger_factory = HandmadeLogger()

    try:
        logger = logger_factory.create(__name__)
        logger.debug('Debug')
        logger.info('Info')
        logger.info('Credentials: abcdefghijklmnop') # Logger filters this record.
        logger.warning('Warn')
        logger.error('Error')
        logger.critical('Critical')
        raise ValueError('Error test')

    except Exception as e:
        ### Error message only
        logger.error(e)
        logger.exception(e, exc_info=False)

        ### With stacktrace
        logger.error(e, exc_info=True)
        logger.exception(e)

        ### Without stacktrace
        logger.error('{}: {}'.format(str(e.__class__.__name__), str(e)))
        logger.error(format_exception_only(type(e), e)[0].rstrip('\n'))


if __name__ == '__main__':
    main()
