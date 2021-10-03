#script.py
import requests, hashlib, datetime, time, sys
try:
    import winsound
    frequency = 2000  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    MissingWinSound= False
except Exception as e:
    MissingWinSound = True

def hashr(website):
    """Downloads the website and checks for the hashes"""
    try:
        response = requests.get(website)
        result = str(hash(response.content))
        return result
    except Exception as e:
        raise

def printer(hash):
    """Prints current datetime and page hash"""
    now = datetime.datetime.now()
    print(now, hash)


def check(hash0, website):
    result = hashr(website)
    printer(result)
    if result != hash0:
        if not MissingWinSound:
            print("# CHANGE!\n")
            winsound.Beep(frequency, duration)
        else:
            print("\a")
    return result;

if __name__ == '__main__':
    """
    Argument list:
        1. url to check
        2. time between each check
    """
    hash0 = '0'
    website = str(sys.argv[1])
    t = int(str(sys.argv[2]))
    while True:
        hash0 = check(hash0, website);
        time.sleep(t)
