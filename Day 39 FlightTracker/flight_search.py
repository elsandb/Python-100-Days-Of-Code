import os
from dotenv import load_dotenv, find_dotenv
import requests
import datetime as dt
load_dotenv(find_dotenv('.env'))

# API keys and endpoints
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.getenv('TEQUILA_API_KEY')


class FlightSearch:
    def __init__(self):
        """FlightSearch is responsible for talking to the Flight Search API."""
        self.from_city_iata = "OSL"
        self.header = {
            "Content-Type": "application/json",
            "apikey": TEQUILA_API_KEY
        }
        self.from_date = dt.datetime.today().strftime("%d/%m/%Y")
        self.to_date = (dt.datetime.today() + dt.timedelta(weeks=26)).strftime("%d/%m/%Y")

    def get_city_iata_code(self, city_name: str) -> str:     # OK #
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=self.header, params=query)
        code = response.json()["locations"][0]["code"]
        return code

    def search_price(self, city_iata: str, price_limit=3000, max_stops=0):
        parameters = {
            "fly_from": "airport:OSL",
            "fly_to": city_iata,
            "date_from": self.from_date,
            "date_to": self.to_date,
            'seats': {'passengers': 1, 'adults': 1, 'children': 0, 'infants': 0},
            "one_per_date": 1,
            "max_stopovers": max_stops,
            "curr": "NOK",
            "locale": "no",
            "price_to": price_limit
        }

        search_response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=parameters, headers=self.header)
        search_response.raise_for_status()
        flight_data = search_response.json()
        return flight_data


# ----------------- Testing -----------------------"
# city_iata = "PAR"
# header = {
#     "Content-Type": "application/json",
#     "apikey": TEQUILA_API_KEY
# }
# search_endpoint = f"https://api.tequila.kiwi.com/v2/search"
# parameters = {
#     "fly_from": "airport:OSL",
#     "fly_to": f"{city_iata}",
#     "dateFrom": f"21/12/2022",
#     "dateTo": f"22/12/2022",
#     'seats': {'passengers': 2, 'adults': 2, 'children': 0, 'infants': 0},
#     "one_per_date": 1
# }
# search_response = requests.get(url=search_endpoint, params=parameters, headers=header)
# search_response.raise_for_status()
# result = search_response.json()["data"][0]["price"]
# print(result)
