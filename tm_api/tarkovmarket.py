import functools, requests, base64, urllib.parse, json
from datetime import datetime

class TarkovMarket:
	def __init__(self) -> None:
		self.base_url = 'https://tarkov-market.com'
		self.session = requests.Session()
		self.has_initialized = False

		self.session.headers.update({
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
			'Referrer': 'https://tarkov-market.com/',
			'Accept': 'application/json, text/plain, */*',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-GB,en',
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-GPC': '1'
		})

		self.has_initialized = self.session.get(self.base_url).status_code == 200

	def api(function: callable) -> callable:
		'Decorator to check API connection.'
		@functools.wraps(function)
		def check_init(self, *args: tuple, **kwargs: tuple) -> object:
			if self.has_initialized == False: return
			return function(self, *args, **kwargs)
		return check_init

	@classmethod
	def decode_payload(self, payload: str) -> dict:
		'Decodes a payload from Tarkov-Market.'
		if len(payload) < 18: return
		
		payload = payload[:9] + payload[18:]
		return json.loads(urllib.parse.unquote(base64.b64decode(payload.encode())))

	@api
	def search(self, search: str, lang: str = 'en', tag: str = None, sort: str = 'name', sort_direction: str = 'desc', trader: str = None, skip: int = 0, limit: int = 20) -> list[dict]:
		'Searches the API.'
		params = {
			'search': search,
			'lang': lang,
			'tag': tag,
			'sort': sort,
			'sort_direction': sort_direction,
			'trader': trader,
			'skip': skip,
			'limit': limit
		}

		response = self.session.get(self.base_url + '/api/items', params = params)
		response_json = response.json()

		if response.status_code != 200 or response_json.get('result') != 'ok': return

		return self.decode_payload(response_json.get('items'))

	@api
	def item_by_url(self, item_url: str) -> dict:
		'''Searches for a specific item using it's URL.'''
		params = {
			'url': item_url
		}

		response = self.session.post(self.base_url + '/api/items/byurl', params)
		response_json = response.json()

		if response.status_code != 200 or response_json.get('result') != 'ok': return

		return self.decode_payload(response_json.get('item'))

	@api
	def get_item(self, item_name: str) -> dict:
		'Uses a searchable name to get item information.'
		item = self.search(item_name, limit=1)
		if item == None or len(item) != 1: return
		return item[0]

	@api
	def get_item_price(self, item_name: str) -> str:
		'Uses a searchable name to get item price. Returns in a parsed string with time since update.'
		item = self.get_item(item_name)

		flea_price = item.get('buyPrices')[0]
		time_delta = datetime.utcnow() - datetime.strptime(flea_price.get('priceUpdated'), '%Y-%m-%dT%H:%M:%S.%fZ')	

		return f'{item.get("enName")}: {flea_price.get("price")} RUB (Updated {round(time_delta.total_seconds() / 60.0)} minutes ago)'