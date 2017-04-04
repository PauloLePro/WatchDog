import os
import re
import psutil

#class SysInfo:

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=", "").replace("'C\n", ""))


# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:4])


# Return % of CPU used by user as a character string
def getCPUuse():
    return psutil.cpu_percent(0.1)


# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:5])

#Return information about wifi and eth

def getInfoWifi(wifiname = 'wlan0'):
    p = psutil.net_if_stats()

    try:
        wifi = p[wifiname]
    except Exception as error:
        print(error)

    return (wifi[0])


def getInfoEth(ethname = 'eth0'):
    p = psutil.net_if_stats()

    try:
        eth = p[ethname]
    except Exception as error:
        print(error)

    return (eth[0])

def getCPUloadPerPID(pid=0):
    if not pid<0:
        try:
            current_process = psutil.Process(pid=pid)
        except psutil.NoSuchProcess:
            return
        current_process_load = current_process.cpu_percent(interval=0.1)
        return current_process_load
    else:
        return


def getCPUloadPerProc():
    i = 0
    processes_info = []
    while i < 2:
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'cpu_percent', 'name'])
                if pinfo['cpu_percent'] > 0.0:
                    processes_info.append(pinfo)
            except psutil.NoSuchProcess:
                pass
        i += 1
    return processes_info


if __name__ == "__main__":

    #getDiskSpace test 1

    regexpDisk = re.compile('(\d{1,3})+%', re.I)

    match = regexpDisk.search(getDiskSpace()[3])
    i = int(match.group(1))

    if i > 30:
        print(i)

    #getCPUtemperature test 2

    j = float(30)

    if j < float(getCPUtemperature()):
        print(getCPUtemperature())

    #getRAMinfo test 3

    a = int(300)

    if a < int(getRAMinfo()[1]):
        print(getRAMinfo()[1])

    #getCPUuse test 4

    b = float(0.0)

    if b < float(getCPUuse()):
        print(getCPUuse())
        print(getCPUloadPerProc())

    #getInfoWifi test 5

    if (getInfoWifi() == True):
        print(True)
    else:
        print(False)

    #getInfoEth test 6

    if (getInfoEth() == True):
        print(True)
    else:
       print(False)