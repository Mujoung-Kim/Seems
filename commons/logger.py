from _init import *

import sys, logging

def get_logger(name):
    handlers = [logging.StreamHandler(sys.stdout)]
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=handlers)

    logger = logging.getLogger(name)
    return logger
