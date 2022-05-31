import pandas as pd
import api
from helpers import *

SS_PATH = 'data/annuals_from_ss.csv'
SHOPIFY_PATH = 'data/shopify_data/16csv_files.csv'
MAN_MARVEL_PATH = 'data/manually_selected_marvel.csv'
ITEM_DATA_PATH = 'data/mondo_items_20220224.csv'
BRAND_ASSURANCE_PATH = 'data/brand_assurance_xref.csv'

SS_COLUMNS = ['Order - Number',
              'Date - Shipped Date',
              'Item - SKU',
              'Item - Name',
              'Item - Qty',
              'Ship To - Company'
              ]

SHOPIFY_COLUMNS = ['Name',
                   'Created at',
                   'Lineitem sku',
                   'Lineitem name',
                   'Lineitem quantity',
                   'Financial Status'
]

item_data_df_COLUMNS = ['sku',
                        'product_type',
                     'published_at',
                     'image_url']
# Load in Data
# get_shopify_data('./shopify_data/', 'csv', save=True) # Uncomment to add more csv files
ss_df = pd.read_csv(SS_PATH, usecols=SS_COLUMNS)
shopify_df = pd.read_csv(SHOPIFY_PATH, usecols=SHOPIFY_COLUMNS)
manual_df = pd.read_csv(MAN_MARVEL_PATH)
item_data_df = pd.read_csv(ITEM_DATA_PATH)
brand_assurance_df = pd.read_csv(BRAND_ASSURANCE_PATH)

# Clean up / work towards items in order data
items = shopify_df[['Lineitem sku', 'Lineitem name', 'Created at']].copy()
items.columns = ['sku', 'name', 'created_at']
items['created_at'] = items['created_at'].apply(lambda x: x.split(' ')[0])
print('Making date objects for created_at columns...')
items['order'] = items['created_at'].apply(get_arrow_date) # Expensive


# Aggregate
agg = {'order': ['min', 'max'], 'created_at': 'count'}
agg_items = items.groupby(['sku', 'name']).agg(agg).reset_index()
agg_items.columns = [' '.join(col).strip() for col in agg_items.columns.values]

# Get unique
unique_items = agg_items.drop_duplicates(subset='sku')

# Pull out easy items with "Marvel" in name
marvel_named = unique_items[unique_items['name'].str.contains(
    'marvel', case=False)]
non_marvel_named = unique_items[~unique_items['name'].str.contains(
    'marvel', case=False)]

# Adds filtered Marvel products to manually selected 
manual_skus = manual_df['sku'].to_list()
manual_marvel = non_marvel_named[non_marvel_named['sku'].isin(manual_skus)]

_all_marvel = pd.concat([marvel_named, manual_marvel])

# Attaches item data, deltas
item_subset = item_data_df[item_data_df_COLUMNS]
all_marvel = pd.merge(_all_marvel, item_subset, on='sku', how='left')
all_marvel['published_at'] = all_marvel['published_at'].apply(
    split_publish_string)
print('Making date objects for published_at columns...')
all_marvel['published_at'] = all_marvel['published_at'].apply(
    get_arrow_date)  # expensive

all_marvel['order_delta'] = all_marvel['order max'] - all_marvel['order min']
all_marvel['lifetime_delta'] = all_marvel['order max'] - all_marvel['published_at']
all_marvel['multiple_publish_dates'] = all_marvel.apply(lambda x: check_for_publishes(
    x['order min'], x['published_at']), axis=1)

# Attaches Inventory
print('Calling inventory API...')
inventory = api.get_inventory()
counts = inventory[['sku', 'quantity_on_hand',
                    'quantity_committed',
                    'quantity_available']]

merged = pd.merge(all_marvel,
                  counts,
                  on='sku',
                  how='left')
merged.sort_values(by='sku', inplace=True)

# Pull in Brand Assurance ids
ids = brand_assurance_df[['Mondo SKU', 'Marvel Brand Assurance Approval #']]
merged = pd.merge(
    merged,
    ids,
    left_on='sku',
    right_on='Mondo SKU',
    how='left'
    
)
merged = merged.drop_duplicates(subset='sku', keep='first').reset_index(drop=True)
merged.drop(columns='Mondo SKU', axis=1, inplace=True)

# Adds Sample information for anything
merged['samples'] = merged.apply(lambda x: calculate_sample_amount(x['quantity_available']) if \
                                 x['lifetime_delta'].days > 356 or x['lifetime_delta'].days < 0 else 'None', axis=1)

rename_dict = {'sku': 'sku', 
               'name': 'name', 
               'order min': 'order_min', 
               'order max': 'order_max', 
               'created_at count': 'order_min_count', 
               'product_type': 'product_type', 
               'published_at': 'published_at', 
               'image_url': 'image_url', 
               'order_delta': 'order_delta',
               'lifetime_delta': 'lifetime_delta', 
               'multiple_publish_dates': 'multiple_publish_dates', 
               'quantity_on_hand': 'quantity_on_hand', 
               'quantity_committed': 'quantity_committed', 
               'quantity_available': 'quantity_available', 
               'samples': 'samples_to_send',
               'Marvel Brand Assurance Approval #': 'brand_assuance_id'}

merged.rename(columns=rename_dict, inplace=True)
# Output
print('Named Marvel Items found: ', len(marvel_named))
print('Unnamed Marvel Items found: ', len(non_marvel_named))
print('Manually Added Marvel Items: ', len(manual_marvel))
print('Total Marvel: ', (len(marvel_named) + len(manual_marvel)))

merged.to_csv(get_download_path('annual_samples.csv'), index=False)
