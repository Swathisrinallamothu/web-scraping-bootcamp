import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


class Google:

    def start_requests(self, ticker, exchange, quantity):

        url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"

        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
        div_element = soup.find(
            "div", attrs={"data-exchange": exchange, "data-last-price": True}
        )
        price = div_element["data-last-price"]
        currency_code = div_element["data-currency-code"]
        # print(currency_code)
        if currency_code != "USD":
            USD_price = self.convert_currency(price, currency_code)
        else:
            USD_price = float(price)

        Market_value = USD_price * quantity
        return [ticker, exchange, quantity, USD_price, Market_value]

    def convert_currency(self, amount, from_currency):
        url = f"https://www.google.com/finance/quote/{from_currency}-USD"
        currency_response = requests.get(url)
        soup = BeautifulSoup(currency_response.content, "html.parser")
        div_element = soup.find("div", {"data-last-price": True})
        price = div_element["data-last-price"]
        USD_price = float(amount) * float(price)
        return round(USD_price, 4)


obj = Google()
results = []
total_market_value = 0
'''In the input.txt file, provide stock information in the format: Ticker Exchange Quantity.'''
with open("input.txt", "r") as file:
    for line in file:
        line = line.strip()
        ticker, exchange, quantity = line.split()
        result = obj.start_requests(
            ticker=ticker, exchange=exchange, quantity=int(quantity)
        )
        market_value = result[-1]
        total_market_value += market_value
        results.append(result)

for result in results:
    allocation = round((result[-1] / total_market_value) * 100, 2)
    result.append(allocation)

table_headers = [
    "Ticker",
    "Exchange",
    "Quantity",
    "Price",
    "Market Value",
    "% Allocation",
]
table = tabulate(results, headers=table_headers, tablefmt="fancy_grid")
print(table)
print(f"Total portfolio value : ${total_market_value}")
