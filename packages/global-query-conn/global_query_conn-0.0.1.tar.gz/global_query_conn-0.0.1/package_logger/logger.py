import logging
import os
from pathlib import Path
from configparser import ConfigParser
import datetime


config = ConfigParser()
config.read('config.ini')
path_backend = config.get('logger', 'path')

class LoggerAplication():
    def __init__(self, tanggal): 
        self._tanggal = tanggal
        
    def Configuration(self):
        tahun = str(self._tanggal.year)
        bulan = str(self._tanggal.month)
        if not Path(f"{path_backend}/{tahun}/{bulan}").is_dir():
            os.makedirs(f"{path_backend}/{tahun}/{bulan}")
        logger = logging.getLogger('Logger Backend Error')
        logger.setLevel(logging.DEBUG)
        path_save_log = f"{path_backend}/{tahun}/{bulan}/{self._tanggal}.log"
        ch = logging.FileHandler(path_save_log, mode='a', encoding=None, delay=False)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def __exit__(self, logger):
        if logger:
            for data_logger in logger.handlers:
                try:
                    data_logger.close()
                    logger.removeHandler(data_logger)
                except Exception as e:
                    print(e)

build_logger = LoggerAplication(datetime.datetime.now().date())

