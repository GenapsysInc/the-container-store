import logging

LOG_FMT = '%(asctime)s - %(name)s:[%(levelname)s] - %(message)s'


def get_logger(name, log_level="INFO"):

    logging.basicConfig(level=log_level, format=LOG_FMT)
    logging.captureWarnings(True)
    logger = logging.getLogger(name)
    return logger

#def set_log_level(log_level="INFO"):
