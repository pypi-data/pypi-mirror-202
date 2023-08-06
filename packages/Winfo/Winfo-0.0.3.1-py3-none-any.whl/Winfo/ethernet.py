from subprocess import check_output

def macaddr():
    """
    DISCLAIMER
    
    May not be true!
    
    If it isn't true, please don't contact us, because this function basically gets it from the getmac-Command in Windows.
    So this basically relies on Windows' Shell.
    
    """
    raw = check_output(["getmac"], shell=True)
    mac = raw.decode().strip().split("\n")[2].split()[0]
    return mac
  
def listadapters():
    raw = check_output(["wmic", "nic", "get", "name"], shell=True)
    rawdecoded = raw.decode()
    maclist = [line.replace("Caption", "").strip() for line in rawdecoded.split("\n")[1:] if line.strip() != ""]
    return maclist