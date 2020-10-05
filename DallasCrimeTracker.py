import requests
import json
import os
import glob
import datetime

DPD_FILE_PREFIX = "DPDFeed_"
DPD_PUBLIC_API_URL = "https://www.dallasopendata.com/resource/9fxf-t2tr.json"
"""Fetches the latest 49 active calls"""



def initializeCacheDir():
    """Initializes cache folder. Creates a new one if it does not exist.
        
        Returns:
            str: Cache Dir (string) if it exists or was created successfully.
        Raises:
            OSError: If active user is unable to create/access cache folder.

    """
    currentDir = os.path.dirname(__file__)
    cacheDir = os.path.join(currentDir, 'cache')
    if (os.path.exists(cacheDir)):
        return cacheDir
    else:
        try:
            os.makedirs(cacheDir)
            return cacheDir
        except OSError as e:
            print("Error: Cannot create cache folder. Please make sure active user have permission to create/access cache folder.")
            print(e.errno)
            exit(1)

def getLastFetchedFile():
    """Retrieves last fetched json file."""
    files = list(filter(os.path.isfile, glob.glob(initializeCacheDir() + "/" +  DPD_FILE_PREFIX + "*")))
    files.sort(key=os.path.getmtime)
    if not files:
        return False
    else:
        return files[0]
    

def getCurrentTime():
    """Get current time. Returns YYYYMMDDDDHHMMSS"""
    currentTime = datetime.datetime.now()
    return currentTime.strftime("%Y%m%d%H%M%S")


def fetchAllActiveCalls (api_url):
    """
    Load active calls and save them into a cached file.
        Parameters:
            api_url (string): API url to call.
        Returns:
            'list' of all active calls
    """
    response = requests.get(api_url)
    if (response.raise_for_status()):
        print("Error loading active calls")
        exit(0)
        return False
    else:
        return response.json()



def getAllNewActiveCalls(all_calls):
    """Returns non-duplicate active calls. If cache file exists, it checks whether calls in the newly fetched file exists in the previously fetched file. Returns the whole list if cache file does not exist and saves the list in cache file."""
    oldFile = getLastFetchedFile()
    if not oldFile:
        newFilePath = os.path.join(initializeCacheDir(), DPD_FILE_PREFIX + getCurrentTime())
        with open(newFilePath, "w") as newFile:
            json.dump(all_calls, newFile)
        return all_calls
    else:
        with open(oldFile, "r") as lastFetchedFile:
            old_calls = json.load(lastFetchedFile)
            new_calls = all_calls
            # Saves new_calls into a new file
            newFilePath = os.path.join(os.path.dirname(oldFile), DPD_FILE_PREFIX + getCurrentTime())
            with open(newFilePath, "w") as newFile:
                json.dump(new_calls, newFile)
                lastFetchedFile.close()
                os.unlink(oldFile)
            return [v for v in old_calls if v not in new_calls]

