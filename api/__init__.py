import pandas as pd

from.amplifier import Amplifier
from.finale import Finale

WAREHOUSES = [Amplifier, Finale]

def get_inventory():
    '''
    - import, clean, and join inventory data to return here
    - Currently needs most of the cleaning in to happen before this.
    
    Currently amp returns array for json key, value pairings and Finale
    returns array of arrays with columns being in 0 index. 

    sku (str)
    description (str) optional 
    quantitiy_on_hand (str)
    quantity_available (str)
    '''
    all_inventory = []
    for warehouse in WAREHOUSES:
        inventory = warehouse().get_inventory()
        all_inventory.append(inventory)
    df_all = pd.concat([pd.DataFrame(i) for i in all_inventory])
    return df_all

if __name__ == '__main__':
    print(get_inventory())