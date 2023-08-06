from subprocess import check_output, CalledProcessError

class ConnectionError(Exception): ...

def publicIP():
    try:
        raw = check_output(["curl", "-X", "GET", "checkip.amazonaws.com", "-s"])
    except CalledProcessError:
        raise ConnectionError("No connection to the internet established!")
    rawdecoded = raw.decode()
    publicip = rawdecoded.replace("\n", "")
    return publicip

def isConnected():
    try:
        check_output(["curl", "-X", "GET", "checkip.amazonaws.com", "-s"])
    except CalledProcessError:
        return False
    else:
        return True

print(publicIP())