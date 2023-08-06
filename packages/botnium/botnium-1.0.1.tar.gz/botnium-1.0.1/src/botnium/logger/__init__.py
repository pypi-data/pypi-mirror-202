import logging
from logging import handlers

logger = logging.getLogger('robot')
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

rotating_file_handler = handlers.RotatingFileHandler(filename='robot.log', maxBytes=1024*1024*5, backupCount=5)
rotating_file_handler.setLevel(logging.DEBUG)
rotating_file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_file_handler)
logger.addHandler(stream_handler)