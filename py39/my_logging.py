import os
from time import gmtime
from logging import \
    config, getLogger, \
    Filter, Formatter, FileHandler, StreamHandler, \
    DEBUG, WARNING

from yaml import safe_load

LOG_FILE_NAME = 'log/test.log'

class FileConfig():
    def __init__(self, config_file=None):
        self.__config_file = config_file
    
    def set(self):
        current_dir = os.path.dirname(__file__)
        with open(current_dir + '/' + self.__config_file) as file:
            _, ext = os.path.splitext(self.__config_file)
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


class StepByStepConfig():
    def __init__(self):
        pass

    def set(self):
        # StreamHandler
        sh_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        default_fmt = Formatter(fmt=sh_fmt, style='%')
        default_fmt.converter = gmtime
        sh = StreamHandler()
        sh.setLevel(WARNING)
        sh.setFormatter(default_fmt)
        sh.addFilter(CredentialsFilter())

        # FileHandler
        fh_fmt = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
        fh_date_fmt = '%Y-%m-%d %H:%M:%S'
        verbose_fmt = Formatter(fmt=fh_fmt, datefmt=fh_date_fmt, style='%')
        verbose_fmt.converter = gmtime
        fh = FileHandler(LOG_FILE_NAME, 'a+')
        fh.setLevel(DEBUG)
        fh.setFormatter(verbose_fmt)
        fh.addFilter(CredentialsFilter())

        # Set handlers to root logger
        logger = getLogger()
        logger.setLevel(DEBUG)
        logger.addHandler(sh)
        logger.addHandler(fh)


class CredentialsFilter(Filter):
    def __init__(self):
        pass

    def filter(self, record) -> bool:
        return self.__check_message(record.getMessage())

    @staticmethod
    def __check_message(message) -> bool:
        return not message.startswith('Credentials')
