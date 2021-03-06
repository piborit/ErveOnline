import logging
from logging.handlers import TimedRotatingFileHandler

def createLogger(name, filename):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = TimedRotatingFileHandler(filename,
                             when="d",
                             interval=1,
                             backupCount=7)
    # handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the file handler to the logger
    logger.addHandler(handler)

    return logger

def getLogger():
    return logging.getLogger()