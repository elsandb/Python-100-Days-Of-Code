import os
import pandas
import datetime as dt
import random
import smtplib

# ---- AUTOMATED BIRTHDAY WISHER ----
# Check the csv file to see if it's someone's birthday today. If yes: Get hold of name and email-address.
# Choose letter 1, 2 or 3 randomly. Replace the name-placeholder with name of person. Send mail.

# ADDRESSES
GMAIL_SERVER_URL = "smtp.gmail.com"
MY_GMAIL = os.getenv('MY_GMAIL')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

# 1. Update the birthdays.csv (put in a valid test-email-address).
# 2. Check if today matches a birthday in birthdays.csv
now_month = dt.datetime.today().month   # Today's month
now_day = dt.datetime.today().day       # Today's day

birthdays = pandas.read_csv("birthdays.csv")    # Read file
b_today = birthdays[(birthdays["day"] == now_day) &
                    (birthdays["month"] == now_month)]  # Filter df on day and month.

if not b_today.empty:   # If there are any birthdays today (if b_today is not an empty DataFrame):
    b_dict = b_today.to_dict(orient="records")  # Convert df to dict.

    # 3. Pick a random letter. Replace [NAME] with the person's name (from birthdays.csv).
    for person in range(0, len(b_dict)):
        with open(f"letter_templates/letter_{random.randint(1, 3)}.txt") as letter:
            letter_text = letter.read()
            new_mail_text = letter_text.replace("[NAME]", b_dict[person]["name"])

            # 4. Send the letter from step 3 to that person's email address.
            with smtplib.SMTP(GMAIL_SERVER_URL) as connection:
                connection.starttls()
                connection.login(user=MY_GMAIL, password=GMAIL_PASSWORD)
                connection.sendmail(from_addr=MY_GMAIL,
                                    to_addrs=b_dict[person]["email"],
                                    msg=f"Subject: Happy birthday {b_dict[person]['name']}\n\n"
                                        f"{new_mail_text}")


# # --------------- Another solution for step 2 ----------------- #
# today = dt.datetime.today()
# today_tuple = (today.month, today.day)      # --> (12, 9)
# data = pandas.read_csv("birthdays.csv")     # Read file.
#
# # Want a dictionary that looks like:
# #       birthdays_dict = {(birthday_month, birthday_day): data_row}
# #       E.g. {(12, 21): Alien,examlpe@gmail.com,1991,12,24}
# birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
#
# if today_tuple in birthdays_dict:
#     birthdays_person = birthdays_dict[today_tuple]
#     # --> Open random letter, replace name and send email to birthday_person.
