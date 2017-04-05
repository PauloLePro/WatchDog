import logging
import logging.handlers
import Sysinfo
import re

class WatchDog:
    def __init__(self):

        self.limiteRAM = 300
        self.limiteDisk = 30
        self.limiteTempCPU = 30.0  # en degré
        self.limiteUseCPU = 2.0 # % de cpu utilisé

        self.main(self._initlog())

    def _initlog(self):

        nomFichierLog = str(Sysinfo.getMacAddress()+'.log')

        # create logger with 'spam_application'
        logger = logging.getLogger('log_application')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fichier = logging.handlers.RotatingFileHandler(nomFichierLog, maxBytes=1048576, backupCount=10) # A 1 Mo il crée un nouveau fichier et peut crée 10 fichier différent
        fichier.setLevel(logging.DEBUG)
        # create console handler with a higher loomg level
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        format = logging.Formatter('%(asctime)s - %(message)s')
        fichier.setFormatter(format)
        console.setFormatter(format)
        # add the handlers to the logger
        logger.addHandler(fichier)
        logger.addHandler(console)

        return logger

    def infoWifi(self):
        if (Sysinfo.getInfoWifi() == True):
            return (True)
        else:
            return (False)

    def infoEth(self):
        if (Sysinfo.getInfoEth() == True):
            return (True)
        else:
            return (False)

    def infoDisk(self):
        regexpDisk = re.compile('(\d{1,3})+%', re.I)

        match = regexpDisk.search(Sysinfo.getDiskSpace()[3])
        disk = int(match.group(1))

        return disk


##########################################################################################################

    def main(self, logger):

        if self.infoWifi() != True:
            logger.info("wifi = False")
            #logger.error("wifi = False")

        if self.infoEth() != True:
            logger.info("eth = False")
            #logger.error("eth = False")

        if self.limiteTempCPU < float(Sysinfo.getCPUtemperature()):
            logger.info('temperature CPU = '+Sysinfo.getCPUtemperature())
            #logger.error(Sysinfo.getCPUtemperature())

        if self.infoDisk() > self.limiteDisk:
            logger.info(self.infoDisk())
            #logger.error(self.infoDisk())

        if self.limiteRAM < int(Sysinfo.getRAMinfo()[1]):
            logger.info('Ram utiliser = '+Sysinfo.getRAMinfo()[1])
            #logger.error(Sysinfo.getRAMinfo()[1])

        if self.limiteUseCPU < float(Sysinfo.getCPUuse()):
            logger.info([self.getCPUuse(), self.getCPUloadPerProc()])
            #logger.error([self.getCPUuse(), self.getCPUloadPerProc()])


if __name__ == '__main__':

    var = WatchDog()
