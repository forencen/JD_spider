import logging.handlers

log_file = '../../log/logger.log'
LOGGING_MSG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] [%(lineno)d] %(message)s'
time_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=0)
time_handler.suffix = '%Y-%m-%d.log'
time_handler.setLevel('INFO')  # error以上的内容输出到文件里面
formatter = logging.Formatter(LOGGING_MSG_FORMAT)
time_handler.setFormatter(formatter)
logger = logging.getLogger('JD')
logger.setLevel('INFO')
logger.addHandler(time_handler)
