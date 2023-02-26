from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# This file will need to use the DataManager, FlightSearch, FlightData, and NotificationManager
# classes to achieve the program requirements.

sheet1_manager = DataManager()
flight_search = FlightSearch()
flight_data_manager = FlightData()

sheet1_data_test = {"cities": [
    {'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 30000, 'maxStops': 0, 'id': 2},
    {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 30000, 'maxStops': 0, 'id': 3},
    {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 30000, 'maxStops': 2, 'id': 4},
    {'city': 'Sydney', 'iataCode': 'SYD', 'lowestPrice': 30000, 'maxStops': 2, 'id': 5},
    {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 30000, 'maxStops': 0, 'id': 6},
    {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 30000, 'maxStops': 2, 'id': 7},
    {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 30000, 'maxStops': 0, 'id': 8},
    {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 30000, 'maxStops': 2, 'id': 9},
    {'city': 'Cape Town', 'iataCode': 'CPT', 'lowestPrice': 3000, 'maxStops': 2, 'id': 10}
]}

# sheet1_data = {'cities': [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 903, 'maxStops': 0, 'id': 2},
#                           {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 672, 'maxStops': 0, 'id': 3},
#                           {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 5229, 'maxStops': 1, 'id': 4},
#                           {'city': 'Sydney', 'iataCode': 'SYD', 'lowestPrice': 6699, 'maxStops': 1, 'id': 5},
#                           {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 1195, 'maxStops': 0, 'id': 6},
#                           {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 5485, 'maxStops': 1, 'id': 7},
#                           {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 2673, 'maxStops': 0, 'id': 8},
#                           {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 4242, 'maxStops': 1, 'id': 9},
#                           {'city': 'Cape Town', 'iataCode': 'CPT', 'lowestPrice': 4886, 'maxStops': 3, 'id': 10}]}

new_sheet1 = sheet1_data_test

# Search prices for all cities in sheet1:
for city in new_sheet1['cities']:
    print("\n", city)  # Print row
    search_result_6_mnd = flight_search.search_price(city["iataCode"], city["lowestPrice"], max_stops=city['maxStops'])

    # Check if any flights are cheaper than old_price.
    flight_dict = flight_data_manager.find_cheapest_date(search_result_6_mnd, city["lowestPrice"])
    if flight_dict == 0:
        print(f"{flight_dict} cheaper flights for {city['city']}\n")
    else:  # Send sms and update sheet1.
        sms_manager = NotificationManager(details=flight_dict)
        city['lowestPrice'] = flight_dict['lowest price']

sheet1_data = new_sheet1
new_sheet1 = None
print(sheet1_data)

# ----------- Todo: When google sheet monthly quota is not used up, continue testing... ----------------------- #
# sheet_data = sheet1_manager.get_sheet_data()
#
# # Update IATA-codes in sheet, if necessary.
# if sheet_data[0]['iataCode'] == '':
#     sheet1_manager.update_all_iata_codes()

# # TEST Search prices for all cities in sheet1:
# for city in sheet1_manager.get_sheet_data():
#     print(city)     # Print row
#     iata_code = city["iataCode"]
#     old_price = city["lowestPrice"]
#     row_id = city["id"]
#     max_stops = city['maxStops']
#
#     # Search cheap flights:
#     search_result_6_mnd = flight_search.search_price(iata_code, old_price, max_stops=max_stops)
#     # Check if any flights are cheaper than old_price.
#     flight_dict = flight_data_manager.find_cheapest_date(search_result_6_mnd, old_price)
#
#     if flight_dict == 0:
#         print(f"{flight_dict} cheaper flights for {city['city']}\n")
#     else:   # Send sms and update sheet1.
#         sms_manager = NotificationManager(details=flight_dict)
#         sheet1_manager.update_a_price(row_id=row_id, price=flight_dict['lowest price'])




# -------------TESTING TESTING TESTING ------------------------------------------- #
# # TEST
# iata_code = sheet1_manager.get_rows()[0]['iataCode']
# old_price = sheet1_manager.get_rows()[0]['lowestPrice']
# print(f"iataCode: {iata_code}, oldPrice: {old_price}")
# search_result_6_mnd = flight_search.search_price(iata_code, old_price)
#
# cheapest_flights = flight_data_manager.find_cheapest_date(search_result_6_mnd, old_price)
# # TEST    with 4 single dates
# # cheapest_flights = {'to_city': 'Paris',
# #                     'iata': 'PAR',
# #                     'date(s)': ['15.01.2023', '08.04.2023', '08.05.2023', '29.05.2023'],
# #                     'lowest price': 902
# #                     }
# # TEST    with 1 single date
# cheapest_flights = {'to_city': 'Paris',
#                     'iata': 'PAR',
#                     'date(s)': '15.01.2023',
#                     'lowest price': 902
#                     }

# print(f"main.py: lowest_price_flight: {flight_dict}\n")
# if flight_dict == 0:
#     pass
# else:
#     # Send sms.
#     print(f"SMS:\nPrice alert: Only {flight_dict['lowest price']} NOK "
#           f"from Oslo-OSL to {flight_dict['to_city']}-{flight_dict['iata']}. "
#           f"Date(s): {flight_dict['date(s)']}.")
#
#     # Update sheet1.
#     row_id = 2      # Todo: in loop, get the row id for the current row on each cycle.
#     sheet1_manager.update_a_price(row_id=row_id, price=flight_dict['lowest price'])
