import pandas as pd
from helpers import get_shopify_data, calculate_sample_amount

SS_PATH = 'data/annuals_from_ss.csv'
SHOPIFY_PATH = 'data/shopify_data/16csv_files.csv'
MAN_MARVEL_PATH = 'data/manually_selected_marvel.csv'
ITEM_DATA_PATH = 'data/mondo_items_20220224.csv'
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
# Load in Data
# get_shopify_data('./shopify_data/', 'csv', save=True) # Uncomment to add more csv files
ss_df = pd.read_csv(SS_PATH, usecols=SS_COLUMNS)
shopify_df = pd.read_csv(SHOPIFY_PATH, usecols=SHOPIFY_COLUMNS)
manual_marvel = pd.read_csv(MAN_MARVEL_PATH)
item_data = pd.read_csv(ITEM_DATA_PATH)

# Clean up
items = shopify_df[['Lineitem sku', 'Lineitem name']]
items.columns = ['sku', 'name']

# Get unique
unique_items = items.drop_duplicates(subset='sku')
print('Unique Items in set: ', len(unique_items))

# Pull out easy items with "Marvel" in name
marvel_named = unique_items[unique_items['name'].str.contains(
    'marvel', case=False)]
non_marvel_named = unique_items[~unique_items['name'].str.contains(
    'marvel', case=False)]

# Adds filtered Marvel products to manually selected 
all_marvel = pd.concat([marvel_named, manual_marvel])

# Output
print('Named Marvel Items found: ', len(marvel_named))
print('Unnamed Marvel Items found: ', len(non_marvel_named))
print('Manually Added Marvel Items: ', len(manual_marvel))
print('Total Marvel: ', (len(marvel_named) + len(manual_marvel)))