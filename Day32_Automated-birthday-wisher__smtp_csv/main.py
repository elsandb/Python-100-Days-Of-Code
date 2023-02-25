import os
import pandas
import datetime as dt
import random
import smtplib

# ---- AUTOMATED BIRTHDAY WISHER ----
# Check the csv file to see if someone has birthday today. If yes: Get hold of name and email-address.
# Choose letter 1, 2 or 3. Read letter. Replace name-holder with name of person --> new letter-text.
# Send mail.

GMAIL_SERVER_URL = "smtp.gmail.com"
MY_GMAIL = os.getenv('MY_GMAIL')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

# 1. Update the birthdays.csv. Put in a valid email address for testing.
# 2. Check if today matches a birthday in the birthdays.csv
pass    # ------ My solution ------- #
now_month = dt.datetime.today().month   # Today's month
now_day = dt.datetime.today().day       # Today's day

birthdays = pandas.read_csv("birthdays.csv")    # Read file
b_today = birthdays[(birthdays["day"] == now_day) & (birthdays["month"] == now_month)]  # Filter df on day and month.

if not b_today.empty:   # If there are any birthdays today (if b_today is not an empty DataFrame):
    b_dict = b_today.to_dict(orient="records")

    # 3. If any birthdays: Pick a random letter. Replace [NAME] with the person's name (from birthdays.csv).
    for person in range(0, len(b_dict)):
        with open(f"letter_templates/letter_{random.randint(1, 3)}.txt") as letter:
            letter_text = letter.read()
            new_mail_text = letter_text.replace("[NAME]", b_dict[person]["name"])

            # 4. Send the letter generated in step 3 to that person's email address.
            with smtplib.SMTP(GMAIL_SERVER_URL) as connection:
                connection.starttls()
                connection.login(user=MY_GMAIL, password=GMAIL_PASSWORD)
                connection.sendmail(from_addr=MY_GMAIL,
                                    to_addrs=b_dict[person]["email"],
                                    msg=f"Subject: Happy birthday {b_dict[person]['name']}\n\n"
                                        f"{new_mail_text}")
