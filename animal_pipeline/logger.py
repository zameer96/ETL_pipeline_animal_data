import logging
import os
from datetime import datetime


class Logger:
    """
    Making custom logger, just incase we need to setup custom notifications like:
        sentry, email/slack/telegeram notification, etc
    """
    def __init__(self, logs_dir='logs'):
        # logs folder check
        os.makedirs(logs_dir, exist_ok=True)
        
        # setup loggers for each type
        self.info_logger = self._setup_logger('info', os.path.join(logs_dir, 'info.log'), level=logging.INFO)
        self.error_logger = self._setup_logger('error', os.path.join(logs_dir, 'info.log'), level=logging.ERROR)
        self.notify_logger = self._setup_logger('notify', os.path.join(logs_dir, 'info.log'), level=logging.INFO)
        self._log_job_time()

    def _setup_logger(self, name, log_file, level=logging.INFO):
        # logger config
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(level)
            handler = logging.FileHandler(log_file)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
        return logger
    
    def _log_job_time(self):
        """
        log job time everytime the job runs just to distinguish between different job runs
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        job_time_message = f"=================JOB TIME: {current_time}================="

        # Force writing the job time message to each log type
        self.info(job_time_message)
        self.error(job_time_message)
        self.notify(job_time_message)

    def info(self, message):
        self.info_logger.info(message)

    def error(self, message):
        """
        Better to add something that notifies user about the error
        """
        self.error_logger.error(message)

    def notify(self, message):
        self.notify_logger.info(message)
