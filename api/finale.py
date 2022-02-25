from config import *
import requests

class Finale:
    """Finale api class to ."""

    def __init__(self):
        self.session = requests.Session()
        self.login = FINALE_AUTH_DICT
        self.authenticate()
        self.report_url = POSTER_INVENTORY_REPORT

    def authenticate(self):
        '''Posts authentication then saves in session.'''

        _aurl = FINALE_ACCOUNT_PATH + FINALE_AUTH_PATH
        self.session.post(_aurl, data=self.login)
        self.session_secret = self.session.cookies['JSESSIONID']
        return self.session

    def get_inventory(self):
        try:
            r = self.session.get(self.report_url)
            response = r.json()[0]['data']
            response[0] = ['sku',
                       'description',
                       'quantity_on_hand',
                       'quantity_available']
            data = []
            for item in response[1:]:
                tmp = {}
                for j in range(len(item)):
                    tmp[response[0][j]] = item[j]
                data.append(tmp)
        except Exception as err:
            print(f'Error getting report: {err}')
            return r
        return data