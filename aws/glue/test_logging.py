import sys
from time import gmtime
import logging

from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'log_level'])
print(args['log_level'])

class HandmadeLogger():
    def __init__(self):
        self.__num_level = getattr(logging, args['log_level'])
        FMT = '%(asctime)s.%(msecs)03d %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s'
        DATE_FMT = '%Y-%m-%d %H:%M:%S'
        verbose_fmt = logging.Formatter(fmt=FMT, datefmt=DATE_FMT, style='%')
        verbose_fmt.converter = gmtime

        self.__sh = logging.StreamHandler()
        self.__sh.setLevel(self.__num_level)
        self.__sh.setFormatter(verbose_fmt)

    def create(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(self.__num_level)
        logger.addHandler(self.__sh)
        logger.addHandler(self.__fh)
        logger.propagate = False


def main():
    try:
        logger = HandmadeLogger().create(__name__)
        logger.debug('Debug')
        logger.info('Info')
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
        logger.error(logging.format_exception_only(type(e), e)[0].rstrip('\n'))


if __name__ == '__main__':
    main()
