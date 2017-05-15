import logging
import logging.handlers
import Sysinfo
import re
import time
import os
from logging.handlers import TimedRotatingFileHandler

#Création de la classe WatchDog
class WatchDog:
    def __init__(self):

        self.logger = self._initlog()

    # Création du fichier de log
    def _initlog(self):

        """"""
        logger = logging.getLogger("Rotating Log")
        logger.setLevel(logging.INFO)

        nomFichierLog = str(Sysinfo.getMacAddress() + '.log')
        file = open(nomFichierLog, "a")
        file.close()

        path = "/opt/testpaul/{}".format(nomFichierLog)

        handler = TimedRotatingFileHandler(path, when="D", interval=1, backupCount=7)
        logger.addHandler(handler)

        format = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(format)

    #    nomFichierLog = str(Sysinfo.getMacAddress()+'.log')

        return logger

    # Vérification pour la Wifi
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

    # Gère l'affichage pour l'info disque (liste 3)
    def infoDisk(self):
        regexpDisk = re.compile('(\d{1,3})+%', re.I)

        match = regexpDisk.search(Sysinfo.getDiskSpace()[3])
        disk = int(match.group(1))

        return disk


##########################################################################################################

    # On gère l'écriture dans le fichier de log des différentes informations
    def write(self):

        if self.infoWifi() != True:
            self.logger.info("wifi = False")
        else:
            self.logger.info("wifi = True")

        if self.infoEth() != True:
            self.logger.info("eth = False")
        else:
            self.logger.info("eth = True")

        self.logger.info('temperature CPU = '+Sysinfo.getCPUtemperature())

        self.logger.info('Utilisation du disque en % ='+str(self.infoDisk()))

        self.logger.info('Ram utiliser = '+Sysinfo.getRAMinfo()[1])

        self.logger.info('Utilisation du CPU en % ='+str(Sysinfo.getCPUuse()))

        #self.logger.info(Sysinfo.getCPUloadPerProc())


#Lance le script
if __name__ == '__main__':

    wd = WatchDog()

    while True:
        wd.write()
        time.sleep(30)
