import logging


class Log(object):
    __logger__ = None

    @staticmethod
    def config_logging(level=logging.INFO):
        """
        Logger format setting and unnecessary log remove
        """
        logging.getLogger().handlers.clear()

        # 'uvicorn --log-config' is broken so we configure in the app.
        #   https://github.com/encode/uvicorn/issues/511
        logging.basicConfig(
            # match gunicorn format
            format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
            datefmt='[%Y-%m-%d %H:%M:%S %z]',
            level=level)

        logging.getLogger('uvicorn.access').handlers.clear()
        logging.getLogger('uvicorn.error').handlers.clear()
        logging.getLogger('uvicorn.access').propagate = True
        logging.getLogger('uvicorn.error').propagate = True

        return logging

    def __init__(self):
        if Log.__logger__:
            logging.info("Logger Instance cannot be instantiated more than once")
        else:
            self.config_logging()
            Log.__logger__ = self.config_logging(level=logging.INFO)


Log()
