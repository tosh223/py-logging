from time import sleep
from multiprocessing.pool import Pool
import logger

PROCESSES = 4
config_file = 'config/logging.yaml'

class LogWriter():
    ###############################################
    def write(self):
        args = [[config_file, num] for num in range(PROCESSES)]
        with Pool(processes=PROCESSES) as p:
            p.map(self.wrapper, args)

    ###############################################
    # Pool Method Wrapper
    def wrapper(self, args):
        return self.write_to_log_file(*args)

    ###############################################
    # Pool Method
    def write_to_log_file(self, config_file, process_num):
        multi_logger = logger.ConfiguredLogger(config_file=config_file).create(f'{__name__}_{process_num}')
        multi_logger.debug(f'process {process_num}: Debug')
        multi_logger.info(f'process {process_num}: Info')
        multi_logger.info(f'process {process_num}: Credentials: abcdefghijklmnop') # Logger filters this record.
        multi_logger.warning(f'process {process_num}: Warning')
        multi_logger.error(f'process {process_num}: Error')
        multi_logger.critical(f'process {process_num}: Critical')

def main():
    log_writer = LogWriter()
    log_writer.write()

###############################################
if __name__ == '__main__':
    main()
