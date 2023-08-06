import logging

class log():
    def __init__(self, module, debug=False):
        self.module = module
        self.logger = logging.getLogger(self.module)
        self.log = logging.StreamHandler()
        self.logformatter = logging.Formatter(fmt='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s', datefmt='%m-%d-%Y %H:%M:%S')

        if debug is True:
            logging.getLogger(self.module).setLevel(logging.DEBUG)
            self.loglevel = 'DEBUG'
        else:
            logging.getLogger(self.module).setLevel(logging.INFO)
            self.loglevel = 'INFO'
        
        self.logger.handlers.clear()
        if not self.logger.hasHandlers():
            self.log.setFormatter(self.logformatter)
            self.logger.addHandler(self.log)

        self.setLevel(self.loglevel)
        

    def setLevel(self, level='DEBUG'):
        try:
            if level.upper() == 'DEBUG':
                logging.getLogger(self.module).setLevel(logging.DEBUG)
                self.loglevel = level.upper()
                self.debug('DEBUG MODE ENABLED.')
            elif level.upper() == 'INFO':
                logging.getLogger(self.module).setLevel(logging.INFO)
                self.loglevel = level.upper()
                self.log('NORMAL MODE ENABLED.')
            elif level.upper() == 'WARNING':
                logging.getLogger(self.module).setLevel(logging.WARNING)
                self.loglevel = level.upper()
            elif level.upper() == 'ERROR':
                logging.getLogger(self.module).setLevel(logging.ERROR)
                self.loglevel = level.upper()
            elif level.upper() == 'CRITICAL':
                logging.getLogger(self.module).setLevel(logging.CRITICAL) 
                self.loglevel = level.upper()
            else:
                return False
            return True
        except:
            return False

    def debug(self, msg):
        try:
            return self.logger.debug(msg)
        except:
            return False

    def info(self, msg):
        try:
            return self.logger.info(msg)
        except:
            return False

    def warning(self, msg):
        try:
            return self.logger.warning(msg)
        except:
            return False

    def error(self, msg):
        try:
            return self.logger.error(msg)
        except:
            return False

    def critical(self, msg):
        try:
            return self.logger.critical(msg)
        except:
            return False