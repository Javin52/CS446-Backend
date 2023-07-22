import logging

def logger():
    logging.basicConfig(level=logging.DEBUG, force=True)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    return log
