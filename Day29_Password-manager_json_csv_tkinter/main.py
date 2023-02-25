from json import JSONDecodeError
import random
import string
from tkinter import *
from tkinter import messagebox
import pandas
import pyperclip
import json

# PASSWORD MANAGER with tkinter
# New passwords will be saved in 'data.json'.

FONT = ("Calibri", 12, "normal")
BG_COLOR = "white"


# ---------------------------- GET PASSWORD ------------------------------------- #
def get_password():
    web_site = web_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Not found", message="No file were found.")
    except JSONDecodeError:
        messagebox.showerror(title="Empty file", message="The password file is emtpy.")
    else:
        if web_site in data:
            email = data[web_site]["email"]  # Get email/username from data.
            email_entry.delete(0, END)  # Delete email/username from email-entry-field.
            email_entry.insert(0, string=email)  # Insert email/username from data.

            password = data[web_site]["password"]
            password_entry.delete(0, END)
            password_entry.insert(0, string=password)
            pyperclip.copy(password)
        else:
            messagebox.showerror(title="Not found", message="No details for the website exists.")

# # --- For practice: Use pandas and get password from data.csv instead:
# def get_password():
#     data = pandas.read_csv("../data.csv")
#     site = data[data["website"] == web_entry.get()]
#     password = site["password"].iat[0]
#     print(password, type(password))
#     password_entry.insert(0, string=password)
#     pyperclip.copy(password)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    special_chars = ["!", "#", "%", "/", "=", "?", ".", "-"]

    new_password = []
    new_password += [random.choice(string.ascii_lowercase) for _ in range(5)]  # Lower case
    new_password += [random.choice(string.ascii_uppercase) for _ in range(1)]  # Upper case
    new_password += [random.choice(string.digits) for _ in range(1)]  # Numbers
    new_password += [random.choice(special_chars) for _ in range(1)]  # Special characters

    random.shuffle(new_password)
    new_password_str = ''.join(new_password)
    password_entry.insert(0, string=new_password_str)
    pyperclip.copy(new_password_str)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_to_json():
    website = web_entry.get()  # Get hold of entries
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    # If any fields are empty give the user a warning:
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Empty fields", message="Please enter info in all fields.")
    else:
        try:
            with open("data.json", mode="r",  encoding='utf-8') as data_file:
                data = json.load(data_file)  # Read 'old' data (--> dict saved in "data").

        except (FileNotFoundError, JSONDecodeError):  # If file not found or empty:
            with open("data.json", "w") as data_file:       # Create new file.
                json.dump(new_data, data_file, indent=4)    # Dump new data to new file.
        else:  # If file was found:
            data.update(new_data)  # Update old data with new data.
            with open("data.json", "w") as data_file:   # Open existing file in write-mode.
                json.dump(data, data_file, indent=4)  # Save updated data.
        finally:
            web_entry.delete(0, END)  # Delete text from entry-boxes
            password_entry.delete(0, END)


# # --- PRACTICE: Use pandas and save password in data.csv instead:
# def save():
#     website = web_entry.get()  # Get hold of entries
#     email = email_entry.get()
#     password = password_entry.get()
#
#     # If any fields are empty give the user a warning:
#     if len(website) == 0 or len(email) == 0 or len(password) == 0:
#         messagebox.showerror(title="Empty fields", message="Please enter info in all fields.")
#         return
#
#     # Check if user is happy with entry:
#     new_input_is_ok = messagebox.askokcancel(title="Happy with the details?",
#                                              message=f"Website: {website}\nEmail/user name: {email}\n"
#                                                      f"Password: {password}")
#     password_list = []
#     new_add = {"website": website,  # Get hold of entries
#                "email": email,
#                "password": password}
#
#     password_list.append(new_add)
#     new_add_df = pandas.DataFrame(password_list)  # Make DataFrame from new_add
#
#     # Concatenate data.csv file with new data:
#     old_password_df = pandas.read_csv("../data.csv")
#     new_password_df = pandas.concat([old_password_df, new_add_df], axis="rows")
#     new_password_df.to_csv("data.csv", index=False)
#
#     # Delete text from entry-boxes
#     web_entry.delete(0, END)
#     password_entry.delete(0, END)


# # --- PRACTICE: Save to txt-file instead:
# def save_to_txt_file():
#     website = web_entry.get()  # Get hold of entries
#     email = email_entry.get()
#     password = password_entry.get()
#
#     # Check id any fields are empty - if so, give warning:
#     if len(website) == 0 or len(email) == 0 or len(password) == 0:
#         messagebox.showerror(title="Empty fields", message="Please enter info in all fields.")
#         return
#
#     # Check if user is happy with entry:
#     new_input_is_ok = messagebox.askokcancel(title="Happy with the details?",
#                                              message=f"Website: {website}\nEmail/user name: {email}\n"
#                                                      f"Password: {password}")
#     if new_input_is_ok:
#         with open("data.txt", "a") as data_txt:
#             data_txt.write(f"{website} | {email} | {password}\n")
#
#         # Delete text from entry-boxes
#         web_entry.delete(0, END)
#         password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk(screenName="Password Manager")
window.configure(bg=BG_COLOR, highlightthickness=0, padx=50, pady=50)
window.title("Password Manager")

# TOP:  CANVAS with LOGO-IMAGE
canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")  # "Create" a PhotoImage from a file. (It's lik importing it).
canvas.create_image(100, 100, image=logo_image)  # The PhotoImage can be used to create a canvas-image.
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", font=FONT, bg=BG_COLOR)
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", font=FONT, bg=BG_COLOR)
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=FONT, bg=BG_COLOR)
password_label.grid(column=0, row=3)

# Entries
web_entry = Entry(width=30, bg=BG_COLOR)
web_entry.grid(column=1, row=1, columnspan=1, sticky="W")
web_entry.focus()

email_entry = Entry(width=35, bg=BG_COLOR)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(0, string="example@gmail.com")

password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky="W")

# Buttons
generate_button = Button(text="Generate Password", command=generate_password, bg=BG_COLOR)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", command=save_to_json, width=36, height=1, bg=BG_COLOR)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

search_password = Button(text="Search", command=get_password, bg=BG_COLOR)
search_password.grid(column=2, row=1, sticky="EW")

window.mainloop()
