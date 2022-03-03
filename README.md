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
order min                          object
order max                          object
order_min_count                    int64
product_type                       object
published_at                       object
image_url                          object
order_delta               timedelta64[ns]
lifetime_delta            timedelta64[ns]
multiple_publish_dates               bool
quantity_on_hand                    int64
quantity_committed                  int64
quantity_available                  int64
samples_to_send                    object
 ```
 
 ### Column Descriptions:
 - **sku**: Item sku
 - **name**: Item name
 - **order_min**: the 'oldest' orders with that skus in the order data.
 - **order_max**: the 'most recent' order with that sku in the order data.
 - **order_min_count**: Count of the arrow min column. Essentially to try and deduce confidence of release date by frequencey of orders on the earliest order date.
 - **product_type**: Item Category from shopify
 - **published_at**: Date that item was most recently published on site.
 - **order_delta**: Delta of most recent order minus the oldest order in order data
 - **lifetime_delta**: Delta of most recent order in order data minus publish date
 - **multiple_publish_dates**: True or False whether or not the earliest order in the data set happened before the publish date. Publish date that is older than the minimum order implies an item was published, sold, hidden, then republished. Making it a lot harder to programatically find the release date.
 - **quantity_on_hand**: Quantity on hand in respective warehouse.
 - **quantity_committed**: Quantity committed to sku in respective warehouse.
 - **quantity_available**: Quantity on hand minus Quantity committed.
 - **samples_to_send**: General action on what samples are needed to send