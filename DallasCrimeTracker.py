import requests
import json

DPD_PUBLIC_API_URL = "https://www.dallasopendata.com/resource/9fxf-t2tr.json"
"""Fetches the latest 49 active calls"""


def getAllActiveCalls (api_url):
    """
    Initialize the class and load the active calls 
    """
    response = requests.get(api_url)
    if (response.raise_for_status()):
        return False
    else:
        return json.loads(response.text)





newObj = getAllActiveCalls(DPD_PUBLIC_API_URL)

print(type(newObj))