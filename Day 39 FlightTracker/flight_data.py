from datetime import datetime as dt


class FlightData:
    """FlightData is responsible for structuring the flight data."""
    def __init__(self):
        self.fly_data = []
        # self.eur_nok_conversion_rate = 10.51

    def find_cheapest_date(self, flight_data: dict, price_limit: int):
        fx_rate = flight_data["fx_rate"]
        fly_data = flight_data["data"]  # Dict
        if len(fly_data) == 0:
            print("fly_data got 0 results.")
            return 0

        # Find the lowest price (including 1 checked bag):
        lowest_price = 0
        for flight in fly_data:
            total_price_nok = int(flight["price"] + ((flight["bags_price"]["1"]) * fx_rate))

            if lowest_price == 0:  # If current loop is the first (lowest_price == 0):
                lowest_price = total_price_nok  # Set new lowest price to compare with.
            else:   # In loops, except the first:
                if total_price_nok < lowest_price:
                    lowest_price = total_price_nok
        print(f"lowest price in search: {lowest_price}")

        # If no cheaper flights: return 0. Else: add flights with the lowest price to cheapest_flights[].
        if lowest_price >= price_limit:
            return 0
        else:
            cheapest_flights = []
            for flight in fly_data:
                total_price_nok = int(flight["price"] + ((flight["bags_price"]["1"]) * fx_rate))
                if total_price_nok == lowest_price:
                    cheapest_flights.append(flight)

        # Make a dict with results for the cheapest flights, and return it.
        result_dict = {
            "to_city": fly_data[0]['cityTo'],
            "iata": fly_data[0]["flyTo"],
            "date(s)": "",
            "lowest price": lowest_price
        }
        if len(cheapest_flights) == 1:    # If only 1 flight with the cheapest price:
            date = dt.strptime(cheapest_flights[0]["utc_departure"].split("T")[0], "%Y-%m-%d")  # Get date
            result_dict["date(s)"] = dt.strftime(date, "%d.%m.%Y")  # Format date, and put it in result-dict.
        else:
            departure_dates = self.get_departure_dates(flight_list=cheapest_flights)
            result_dict["date(s)"] = departure_dates

        return result_dict

    def get_departure_dates(self, flight_list):
        """Accept a list of dictionaries, where each dict is a flight (results from FlightSearch).
        Return departure-dates (str) as a list of one or more range(s) of consecutive dates. E.g.
        if you pass a flight_list where the dates are [2022-10-01, 2022-10-02, 2022-10-03, 2022-11-05], it will
        be returned as [01.10.2022 - 03.10.2022, 05.11.2022]."""

        # Todo: Find a simpler way to get a list of consecutive dates ranges.

        fly_list = flight_list
        dates_str = [flight["utc_departure"].split("T")[0] for flight in fly_list]  # List of dates <str>.
        dates = [dt.strptime(d, "%Y-%m-%d") for d in dates_str]  # List of dates <type datetime>.

        dates.sort()  # Sort dates
        date_ints = [d.toordinal() for d in dates]  # toordinal() returns the day count from 01/01/01 as <int>.
        ranges = {}  # Dict that will be filled with ranges of consecutive dates.
        a_range = []  # Variable that will be filled with one range of consecutive dates, with key = "{j}".
        j = 1  # The first range-number
        prev = 0  # Previous date_int
        index = 0  # Index of date_ints

        for i in date_ints:  # Iterate through date integers.
            if i + 1 == date_ints[index] + 1 and i - 1 == prev:  # If in sequence with last date in a_range (== prev)
                a_range.append(dates[index].strftime("%d.%m.%Y"))  # Append to a_range.
            elif prev == 0:  # Append first date to 'a_range' list since 'prev' has not been updated.
                a_range.append(dates[index].strftime("%d.%m.%Y"))
            else:
                ranges.update(
                    {f'{j}': tuple(a_range)})  # For integer not in sequence -> update dictionary with new range.
                a_range = []  # Cleare a_rage, so the next date will append to a new range.
                j += 1  # Go to next range number (since we now is finished with one).
                a_range.append(dates[index].strftime("%d.%m.%Y"))
            index += 1  # Update index (so that next loop will use next index in date_ints).
            prev = i  # Update prev (so that next loop "knows" what the previous date was).
        ranges.update({f'{j}': tuple(a_range)})

        departure_dates = []
        for tuples in ranges.values():
            if len(tuples) == 1:
                departure_dates.append(tuples[0])
            else:
                departure_dates.append(f"{tuples[0]} - {tuples[-1]}")
        return ', '.join(departure_dates)