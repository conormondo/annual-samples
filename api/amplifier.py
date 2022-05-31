from struct import unpack
import requests
from config import AMP_HEADERS, AMP_INVENTORY_URL, AMP_ITEMS_URL

def unpack_inventory(item_dict):
    '''Unpacks the inventory that api returns as json object'''
    inventory_dict = item_dict.get('inventory', None)
    if not inventory_dict:
        print('ERROR')
        return
    for key in inventory_dict.keys():
        item_dict[key] = inventory_dict.get(key)
    del item_dict['inventory']
    return item_dict

def filter_items(*item_dicts):
    '''Filters to only the wanted fields'''
    arr = []
    filter_cols = ['sku',
                   'description',
                   'quantity_on_hand',
                   'quantity_available',
                   'quantity_committed',
                   'made_to_order',
                   'location']
    for _id in item_dicts:
        unpacked = unpack_inventory(_id)
        tmp = {}
        for col in filter_cols:
            tmp[col] = unpacked[col]
        arr.append(tmp)
    return arr

class Amplifier:
    
    def __init__(self):
        pass
    
    # def get_inventory(self):
    #     url = AMP_INVENTORY_URL
    #     request = requests.get(url, headers=AMP_HEADERS)
    #     if request.status_code > 200:
    #         print('ERROR: ', request.status_code)
    #     else:
    #         items = self.get_items()
            
    #         return request.json()['inventory']
        
    def get_inventory(self):
        '''
        Only to get item names
        Returns list of item info as dict
        '''
        
        pages = []
        url = AMP_ITEMS_URL
        params = {'per_page':200}
        request = requests.get(url, headers=AMP_HEADERS, params=params)
        json_data = request.json()
        pages.append(json_data.get('data'))
        first_page = json_data.get('page')
        total_pages = json_data.get('total_pages')
        
        for r in range(first_page, total_pages + 1):
            current_page = first_page + r
            params['page'] = str(current_page)
            request = requests.get(url, headers=AMP_HEADERS, params=params)
            pages.append(request.json().get('data'))
        
        # Flattens
        tmp_items = [item for page in pages for item in page]
        for i in tmp_items:
            i['location'] = self.__str__()
        # Unpacks inventory
        self.items = filter_items(*tmp_items)
        return self.items
    
    def __str__(self) -> str:
        return 'Amplifier'
    
if __name__ == '__main__':
    api = Amplifier()
    items = api.get_items()