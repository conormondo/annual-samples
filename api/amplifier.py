import requests
from config import AMP_HEADERS, AMP_INVENTORY_URL

class Amplifier:
    
    def __init__(self):
        pass
    
    def get_inventory(self):
        url = AMP_INVENTORY_URL
        request = requests.get(url, headers=AMP_HEADERS)
        if request.status_code > 200:
            print('ERROR: ', request.status_code)
        else:
            return request.json()['inventory']