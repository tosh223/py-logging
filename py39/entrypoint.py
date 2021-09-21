import argparse
from my_logging import CredentialsFilter, FileConfig, StepByStepConfig
from logging import getLogger
from traceback import format_exception_only

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config", help="logger config file", type=str, default=None
    )

    return parser.parse_args()

def main():
    logger = getLogger(__name__)
    logger.addFilter(CredentialsFilter())

    try:
        logger.debug('Debug')
        logger.info('Info')
        logger.critical('Credentials: abcdefghijklmnop') # Logger filters this record.
        logger.warning('Warning')
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
    config_file = get_args().config
    if config_file:
        file_config = FileConfig(config_file=config_file)
        file_config.set()
    else:
        handmade_config = StepByStepConfig()
        handmade_config.set()

    main()