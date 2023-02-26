import os
import requests
# from twilio.rest import Client
from dotenv import load_dotenv, dotenv_values, find_dotenv
load_dotenv(find_dotenv('.env'))

# -------------- Weather ------------------------------- #
# Weather API website: https://openweathermap.org/api/one-call-3
OMW_endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = os.getenv('API_KEY')

# ------------------ SMS (Twilio) --------------------------#
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
MY_PHONE_NR = os.getenv('MY_PHONE_NR')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')

# oslo_latitude = 59.913868
# oslo_longitude = 10.752245
test_lat = 40.416775    # Find place where it's raining now at https://www.ventusky.com/nb/madrid
test_long = -3.703790

parameters = {
    "lat": test_lat,
    "lon": test_long,
    "appid": api_key,
    "units": "metric",
    "exclude": "current,minutely,daily,alerts"
}

response = requests.get(url=OMW_endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]    # Get the first 12 hours (0 to 11). --> List of dictionaries.

will_rain = False
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    print("Rain")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Rain (or snow) 🌧️❄️ Bring an umbrella (or skis).",
        from_=TWILIO_PHONE,
        to=MY_PHONE_NR
    )
    print(message.status)
else:
    print('No rain')
