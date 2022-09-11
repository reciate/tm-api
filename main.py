from tm_api import TarkovMarket

def main() -> None:
	market = TarkovMarket()

	if market.has_initialized == False:
		print('Could not initialize.')
		return

	for entry in market.search(None, limit=5, sort='change24'):
		print(f'{entry.get("enName")}: {entry.get("avgDayPrice")} RUB ({entry.get("change24")}% change in 24h)')

	print(market.get_item_price('azimut'))

main()