import os
import requests
import datetime as dt
import time
import smtplib

# OBJECTIVE
# If the ISS (International Space Station) is close to my current position, AND it is currently dark
#  ➡ email me and tell me to look up. Run the code every 60 sec.

# USEFUL LINKS
# ISS current position API site: http://open-notify.org/Open-Notify-API/ISS-Location-Now/
# Find your latitude and longitude here: https://www.latlong.net/
# Sunset-Sunrise API documentation: https://sunrise-sunset.org/api

GMAIL_SERVER_URL = "smtp.gmail.com"
MY_GMAIL = os.getenv('MY_GMAIL')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

MY_LAT = 44.5987  # Latitude
MY_LONG = -88.2671  # Longitude


def close_to_iss():
    """Returns true if ISS is currently """
    # Get ISS current position:
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()  # --> Raise error if response != 200.
    iss_latitude = float(response_iss.json()["iss_position"]["latitude"])   # --> 129.7400 <class 'float'>
    iss_longitude = float(response_iss.json()["iss_position"]["longitude"])
    print(iss_latitude, iss_longitude)
    if iss_latitude - 5 <= MY_LAT <= iss_latitude + 5:
        if iss_longitude - 5 <= MY_LONG <= iss_longitude + 5:
            return True
    else:
        return False


def currently_dark():
    # sunset and sunrise at my position (MY_LAT, MY_LONG).
    parameters = {          # Parameter dict, based on keys in the Sunrise-Sunset API documentation.
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0      # 0 = Get time-value formated according to ISO 8601 (2022-12-09T08:02:18+00:00).
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters).json()
    response.raise_for_status()
    data = response.json()

    # Get sunrise and sunset hour for :
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])   # --> Hour format: 08
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    now_hour = dt.datetime.now().hour   # Hour right now

    if now_hour >= sunset_hour or now_hour <= sunrise_hour:     # If after sunset, or before sunrise (= if dark).
        return True
    else:
        return False


while True:
    if close_to_iss() and currently_dark():
        print("Look up.")
        with smtplib.SMTP("smtp.gmail.com") as connection:      # Send mail
            connection.starttls()
            connection.login(user=MY_GMAIL, password=GMAIL_PASSWORD)
            connection.sendmail(
                from_addr=MY_GMAIL,
                to_addrs=MY_GMAIL,
                msg="Subject: Look up to see ISS\n\n"
                    "The ISS is currently close to you, and it is dark outside.\n"
                    "Look up :)")
    else:
        print(':(')
    time.sleep(60)
