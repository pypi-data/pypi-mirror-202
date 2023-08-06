from subprocess import check_output

def getmanufacturer():
    raw = check_output(["wmic", "memorychip", "get", "caption"])
    rawdecoded = raw.decode()
    getmanu = rawdecoded.strip("Caption").rstrip("\n").replace("\n", "")
    return getmanu

def getcapacityMB():
    raw = check_output(["wmic", "computersystem", "get", "totalphysicalmemory"])
    rawdecoded = raw.decode().lstrip("TotalPhysicalMemory").rstrip("\n")
    getcapMB = int(rawdecoded) / 1024 ** 2
    return int(getcapMB)

def getcapacityGB():
    raw = check_output(["wmic", "computersystem", "get", "totalphysicalmemory"])
    rawdecoded = raw.decode().lstrip("TotalPhysicalMemory").rstrip("\n")
    getcapGB = int(rawdecoded) / 1024 ** 3
    return float(getcapGB)

def getSpeed():
    raw = check_output(["wmic", "memorychip", "get", "Speed"])
    rawdecoded = raw.decode().lstrip("Speed").rstrip("\n")
    getspeed = rawdecoded.replace("\n", "")
    return float(rawdecoded)