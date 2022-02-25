import base64

# Amplifier
AMP_INVENTORY_URL = 'https://api.amplifier.com/reports/inventory/current'
AMP_API_KEY =  'df195b54-72d3-470e-b362-55c38f0780a5'


authentication_format = (AMP_API_KEY).encode('ascii')
auth_header = 'Basic ' + \
    base64.b64encode(authentication_format).decode('utf-8')
AMP_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': auth_header
    }

# Finale
FINALE_USER = 'Conor'
FINALE_PASS = 'GetTheKnife13!'
FINALE_AUTH_DICT = {
    "username": FINALE_USER,
    "password": FINALE_PASS
}
FINALE_ACCOUNT_PATH = 'https://app.finaleinventory.com/'
FINALE_AUTH_PATH = 'mondotees/api/auth'

POSTER_INVENTORY_REPORT = 'https://app.finaleinventory.com/mondotees/doc/report/pivotTable/1645740764469/Report.json?format=json&data=stock&attrName=%23%23user106&rowDimensions=~kpnNAf7AzP7AwMDAwMCZzQHUwMz-wMDAwMDA&metrics=~kpnZSXByb2R1Y3RTdG9ja0NvbHVtblF1YW50aXR5T25IYW5kVW5pdHNNb25kb3RlZXNhcGlmYWNpbGl0eTEwMDAwQ29uc29saWRhdGWwUXVhbnRpdHkgb24gaGFuZMz-wMDAwMDAmdlNcHJvZHVjdFN0b2NrQ29sdW1uQXZhaWxhYmxlVG9Qcm9taXNlVW5pdHNNb25kb3RlZXNhcGlmYWNpbGl0eTEwMDAwQ29uc29saWRhdGW0QXZhaWxhYmxlIHRvIHByb21pc2XM_sDAwMDAwA&filters=W1sicHJvZHVjdENhdGVnb3J5IixudWxsXSxbInN0b2NrTG9jYXRpb24iLFsiL21vbmRvdGVlcy9hcGkvZmFjaWxpdHkvMTAwMDAiXV0sWyJzdG9ja01hZ2F6aW5lIiwiL21vbmRvdGVlcy9hcGkvZmFjaWxpdHkvMTAwMDEiXV0%3D&reportTitle=Baker+Inventory+Only'
