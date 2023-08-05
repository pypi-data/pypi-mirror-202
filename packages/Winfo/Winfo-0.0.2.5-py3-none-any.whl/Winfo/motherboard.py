from subprocess import check_output

def getname():
    raw = check_output(["wmic", "baseboard", "get", "product"], shell=True)
    rawdecoded = raw.decode()
    getboard = rawdecoded.replace("Product", "").replace("\n", "")
    return getboard
def getmanufacturer():
    raw = check_output(["wmic", "baseboard", "get", "manufacturer"], shell=True)
    rawdecoded = raw.decode()
    getmanu = rawdecoded.replace("Manufacturer", "").replace("\n", "")
    return getmanu