import logging
import os

def _setup_logger():
    logger = logging.getLogger('dataforge')
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(root, 'error.log')

    handler = logging.FileHandler(log_path, encoding='utf-8')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    ))
    logger.addHandler(handler)
    return logger


_logger = _setup_logger()


def log_info(msg: str):
    _logger.info(msg)


def log_warning(msg: str):
    _logger.warning(msg)


def log_error(msg: str, exc: Exception = None):
    if exc:
        _logger.error(msg, exc_info=exc)
    else:
        _logger.error(msg)
