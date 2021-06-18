from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, WARN
# import traceback

class TestLogger():
    def __init__(self):
        self.logger = getLogger(__name__)
        fmt = Formatter('%(asctime)s %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s]%(message)s')

        sh = StreamHandler()
        sh.setLevel(WARN)
        sh.setFormatter(fmt)

        fh = FileHandler('test.log', 'a+')
        fh.setLevel(DEBUG)
        fh.setFormatter(fmt)

        self.logger.setLevel(DEBUG)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
        self.logger.propagate = False

def main():
    try:
        logger = TestLogger().logger
        logger.debug('Debug')
        logger.info('Info')
        logger.warning('Warn')
        logger.error('Error')
        raise ValueError('Error test')
        # raise ZeroDivisionError('Error test')
    except Exception as e:
        ### Error class and message only
        logger.error('{}: {}'.format(str(e.__class__.__name__), str(e)))
        # logger.error(traceback.format_exception_only(type(e), e)[0].rstrip('\n'))

        ### With stacktrace
        # logger.exception(e)

if __name__ == '__main__':
    main()
