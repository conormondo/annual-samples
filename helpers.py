import glob
from operator import inv
import zipfile
import pandas as pd

# Gets CSVs from ZIPs
def unzip_files():
    files = glob.glob('./shopify_data/*.zip')
    for file in files:
        csv_file = file.split('.')
        csv_file[-1] = 'csv'
        csv_file = '.'.join(csv_file)
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall('./shopify_data/')
        
# Combines CSVs for dataframes
def get_shopify_data(path, filetype, save=False):
    df_list = []
    file_path = '*.'.join([path, filetype.lower()])
    files = glob.glob(file_path)
    
    for file in files:
        df = pd.read_csv(file, dtype=str)
        df_list.append(df)
        
    if len(df_list) > 0:
        print(f'Reading {len(df_list)} {filetype} files from {path}')
        _concat = pd.concat(df_list)
        if save:
            save_name = f'./shopify_data/{len(df_list)}{filetype}_files.csv'
            _concat.to_csv(save_name, index=False)
        return _concat
    else:
        print(f'Unable to get {filetype} from {path}')
        return None
# Gets How many samples to send
def calculate_sample_amount(inventory):
    ''' Takes inventory level and returns the 'action' for annual samples.'''
    inv = int(inventory)
    if inv > 250:
        return 'Send 30'
    if inv >= 2:
        return 'Send 2'
    else:
        return 'Replace sku'
    
if __name__ == '__main__':
    get_shopify_data('./shopify_data/', 'csv')
