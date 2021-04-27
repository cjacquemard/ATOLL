import sys
import os
import inspect
import logging

def get_logger():
    logging.basicConfig()
    caller_module_name = os.path.basename(inspect.getmodule(inspect.stack()[-1][0]).__file__).split('.')[0]

    logger = logging.getLogger(caller_module_name)
    logger.setLevel(logging.INFO)

    return logger


def get_amberhome():
    if 'AMBERHOME' in os.environ:
        amberhome = os.environ['AMBERHOME']
    else:
        logger.critical('"$AMBERHOME" is not defined')
        sys.exit(1)

    if not os.path.isdir(amberhome):
        logger.critical('"$AMBERHOME" directory defined as "{}" is not found'.format(amberhome))
        sys.exit(1)

    return amberhome