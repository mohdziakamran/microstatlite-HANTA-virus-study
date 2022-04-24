import multiprocessing, logging

def create_logger(appname):
    
    logger = multiprocessing.get_logger()
    logger.__setattr__('name',appname)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s| %(levelname)s| %(processName)s] - %(name)s : %(message)s')
    file_handler = logging.FileHandler('logfile.log')
    file_handler.setFormatter(formatter)
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # this bit will make sure you won't have 
    # duplicated messages in the output
    if not len(logger.handlers): 
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


if __name__=='__main__':
    pass