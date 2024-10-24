import logging
import os

class LogHandler:
    LEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
    FORMAT = '%(asctime)s [%(levelname)5s] %(filename)s :: %(funcName)s() - %(message)s'

    def createSchedulerLogger(self, processConfig, configLogs):
        loggerName = f'{processConfig.id}_SCHEDULER'
        fileName = f'{processConfig.id}.txt'
        filePath = os.path.join(configLogs.schedulerLogDir, fileName)
        return self.createLogger(loggerName, filePath, configLogs.enabled)

    def createProcessLogger(self, processConfig, configLogs, nowDatetime): 
        loggerName = f'{processConfig.id}_PROCESS'
        fileName = f'{nowDatetime.strftime("%Y%m%d-%H%M%S")}_{processConfig.id}.txt'
        filePath = os.path.join(configLogs.processLogDir, fileName)
        return self.createLogger(loggerName, filePath, configLogs.enabled)

    def createLogger(self, name, filePath, fileLoggingEnabled):
        logger = logging.getLogger(name)
        logger.setLevel(LogHandler.LEVEL)

        if fileLoggingEnabled:
            fh = logging.FileHandler(filePath)
            fh.setFormatter( logging.Formatter(LogHandler.FORMAT) )
            if logger.hasHandlers():
                for h in list (logger.handlers):
                    logger.removeHandler(h)
            logger.addHandler(fh)

        logging.debug(f'name={logger.name}, level={logger.level}, handlers={logger.handlers}')

        return logger
