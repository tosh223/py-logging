from time import sleep
from multiprocessing.pool import Pool
from my_logging import CredentialsFilter, FileConfig
from logging import getLogger

PROCESSES = 4
CONFIG_FILE_NAME = 'config/logging.yaml'

class LogWriter():
    def __init__(self, logger):
        self.__logger = logger

    ###############################################
    def write(self):
        args = [[num] for num in range(PROCESSES)]
        with Pool(processes=PROCESSES) as p:
            p.map(self.wrapper, args)

    ###############################################
    # Pool Method Wrapper
    def wrapper(self, args):
        return self.write_to_log_file(*args)

    ###############################################
    # Pool Method
    def write_to_log_file(self, process_num):
        self.__logger.debug(f'process {process_num}: Debug')
        self.__logger.info(f'process {process_num}: Info')
        self.__logger.critical(f'process {process_num}: Credentials: abcdefghijklmnop') # Logger filters this record.
        self.__logger.warning(f'process {process_num}: Warning')
        self.__logger.error(f'process {process_num}: Error')
        self.__logger.critical(f'process {process_num}: Critical')

def main():
    logger = getLogger('__name__')
    logger.addFilter(CredentialsFilter())    
    log_writer = LogWriter(logger)
    log_writer.write()

###############################################
if __name__ == '__main__':
    file_config = FileConfig(config_file=CONFIG_FILE_NAME)
    file_config.set()
    main()
