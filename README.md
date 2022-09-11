# tm-api
A wrapper for the Tarkov-Market Public API.

## Requirements
* Python >= 3.9
* pip

## Installation
### Python
* In the tm-api folder, run `pip install -r requirements.txt`.

## Usage
* `main.py` contains example usage.
* Each entry in `TarkovMarket.search()` or `TarkovMarket.item_by_url()` contains the following keys:
```python
['uid', 'avgDayPrice', 'avgWeekPrice', 'change24', 'change7d', 'enImg', 'enName', 'price', 'ruImg', 'ruName', 'size', 'tags', 'updated', 'url', 'wikiIcon', 'wikiImg', 'wikiName', 'wikiUrl', 'shortName', 'priceUpdated', 'traderName', 'traderPrice', 'traderPriceCur', 'bsgId', 'cnName', 'cnShortName', 'ruShortName', 'deName', 'deShortName', 'frName', 'frShortName', 'esName', 'esShortName', 'basePrice', 'czName', 'czShortName', 'huName', 'huShortName', 'trName', 'trShortName', 'grid', 'canSellOnFlea', 'name', 'search', 'pricePerSlot', 'avgDayPricePerSlot', 'avgWeekPricePerSlot', 'updatedLongTimeAgo', 'haveMarketData', 'traderPriceRub', 'buyPrices', 'sellPrices', 'fee', 'trader_bb_profit']
```