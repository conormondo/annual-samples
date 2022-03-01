import pandas as pd
from helpers import *

SS_PATH = 'data/annuals_from_ss.csv'
SHOPIFY_PATH = 'data/shopify_data/16csv_files.csv'
MAN_MARVEL_PATH = 'data/manually_selected_marvel.csv'
item_data_df_PATH = 'data/mondo_items_20220224.csv'
AMP_INVENTORY_PATH = ''
FIN_INVENTORY_PATH = ''

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
                     'published_at']
# Load in Data
# get_shopify_data('./shopify_data/', 'csv', save=True) # Uncomment to add more csv files
ss_df = pd.read_csv(SS_PATH, usecols=SS_COLUMNS)
shopify_df = pd.read_csv(SHOPIFY_PATH, usecols=SHOPIFY_COLUMNS)
manual_df = pd.read_csv(MAN_MARVEL_PATH)
item_data_df = pd.read_csv(item_data_df_PATH)

# Clean up / work towards items in order data
items = shopify_df[['Lineitem sku', 'Lineitem name', 'Created at']].copy()
items.columns = ['sku', 'name', 'created_at']
items['created_at'] = items['created_at'].apply(lambda x: x.split(' ')[0])
items['arrow'] = items['created_at'].apply(get_arrow_date) # Expensive


# Aggregate
agg = {'arrow': ['min', 'max'], 'created_at': 'count'}
agg_items = items.groupby(['sku', 'name']).agg(agg).reset_index()
agg_items.columns = [' '.join(col).strip() for col in agg_items.columns.values]
print(agg_items.columns)

# Get unique
unique_items = agg_items.drop_duplicates(subset='sku')
print('Unique Items in set: ', len(unique_items))

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
all_marvel['published_at'] = all_marvel['published_at'].apply(
    get_arrow_date)  # expensive

all_marvel['order_delta'] = all_marvel['arrow max'] - all_marvel['arrow min']
all_marvel['lifetime_delta'] = all_marvel['arrow max'] - all_marvel['published_at']
all_marvel['multiple_publish_dates'] = all_marvel.apply(lambda x: check_for_publishes(
    x['arrow min'], x['published_at']), axis=1)

# Output
print('Named Marvel Items found: ', len(marvel_named))
print('Unnamed Marvel Items found: ', len(non_marvel_named))
print('Manually Added Marvel Items: ', len(manual_marvel))
print('Total Marvel: ', (len(marvel_named) + len(manual_marvel)))

print(all_marvel)