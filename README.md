# Marvel Annual Samples Reporting
An attempt at somewhat simple Marvel Annual Sample reporting
## Requirements
- [Python >= v3.0.0](https://www.python.org/downloads/)
- [Order data for the period of time you are looking for samples in /data/ directory](https://mondo-30.myshopify.com/admin/orders?inContextTimeframe=today)
- [Item export of all products from Shopify.](https://mondo-30.myshopify.com/admin/products?selectedView=all)
## Usage:
```
python main.py
```
## Reading the report
Will probably rename these columns
### Column Data Types
```
sku                                object
name                               object
arrow min                          object
arrow max                          object
created_at count                    int64
published_at                       object
order_delta               timedelta64[ns]
lifetime_delta            timedelta64[ns]
multiple_publish_dates               bool
 ```
 ### Column Descriptions:
 - sku: Item sku
 - name: Item name
 - arrow min: the 'oldest' orders with that skus in the order data.
 - arrow max: the 'most recent' order with that sku in the order data.
 - created_at count: Count of the arrow min column. Essentially to try and deduce confidence of release date by frequence of orders on the earliest order date.
 - published_at: Date that item was most recently published on site.
 - order_delta: Delta of most recent order minus the oldest order in order data
 - lifetime_delta: Delta of most recent order in order data minus publish date
 - multiple_publish_dates: True or False whether or not the earlist order in data set happened before the publish date. Publish date that is older than the minimum order implies an item was published, sold, hidden, then republished. Making it a lot harder to programatically find the release date.