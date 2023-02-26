import os
import requests
from flight_search import FlightSearch
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))
SHEET1_ENDPOINT = os.getenv('SHEET1_ENDPOINT')          # From Google sheets.
SHEETY_BEARER_TOKEN = os.getenv('SHEETY_BEARER_TOKEN')  # From Google sheets.


class DataManager:
    """This class is responsible for talking to the Google Sheet (sheet1)."""
    def __init__(self):
        self.sheet1_endpoint = SHEET1_ENDPOINT
        self.sheet1_token = SHEETY_BEARER_TOKEN
        self.header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
        }
        self.sheet1_data = {}

    def get_sheet_data(self):
        """Returns rows in sheet1 as a list of dicts."""
        sheet1_response = requests.get(url=self.sheet1_endpoint, headers=self.header)
        list_of_rows = sheet1_response.json()["sheet1"]
        return list_of_rows

    def update_all_iata_codes(self):
        location_search = FlightSearch()    # Connect with FlightSearch-class in flight_search.py
        for row in self.get_sheet_data():
            iata_code = location_search.get_city_iata_code(city)  # Search iata_code for city
            # Update row with iata-code:
            row_input = {"sheet1": {"iataCode": f"{iata_code}"}}
            insert_iata_code = requests.put(url=f"{SHEET1_ENDPOINT}/{row['id']}", json=row_input, headers=self.header)
            insert_iata_code.raise_for_status()

    def update_a_price(self, row_id: int, price: int):
        row_input = {"sheet1": {"lowestPrice": price}}
        insert_price = requests.put(url=f"{SHEET1_ENDPOINT}/{row_id}", json=row_input, headers=self.header)
        insert_price.raise_for_status()
        print(insert_price.text)