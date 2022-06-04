import logging
logging.basicConfig(filename='logger_forest.log',level=logging.INFO,format='(%(levelname)s %(message)s %(asctime)s)')
#logger for error
def logging_error(err):
    logging.error("there was error " +str(err))


def logging_info(info):
    logging.info(info)
