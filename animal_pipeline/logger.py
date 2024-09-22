import logging
import os


class Logger:
    """
    Making custom logger, just incase we need to setup custom notifications like:
        sentry, email/slack/telegeram notification, etc 
    """
    def __init__(self, logs_dir='logs'):
        # logs folder check
        os.makedirs(logs_dir, exist_ok=True)

        # setup loggers for each type
        self.info_logger = self._setup_logger('info', os.path.join(logs_dir, 'info.log'))
        self.error_logger = self._setup_logger('error', os.path.join(logs_dir, 'error.log'), level=logging.ERROR)
        self.notify_logger = self._setup_logger('notify', os.path.join(logs_dir, 'notify.log'))

    def _setup_logger(self, name, log_file, level=logging.INFO):
        # logger config
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(level)
            handler = logging.FileHandler(log_file)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
        return logger

    def info(self, message):
        self.info_logger.info(message)

    def error(self, message):
        """
        Better to add something that notifies user about the error
        """
        self.error_logger.error(message)

    def notify(self, message):
        self.notify_logger.info(message)
