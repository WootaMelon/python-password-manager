from tkinter import *
from tkinter import messagebox
import pyperclip
import json
from password_generator import password_generator

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_entry_generation():
    generated_password = password_generator()
    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)


# ---------------------------- SAVE CREDENTIALS ------------------------------- #


def save_credentials():
    website_name = website_entry.get()
    email_username = email_user_entry.get()
    password = password_entry.get()
    data_dict = {website_name: {"email/username": email_username, "password": password}}

    if len(website_name) == 0 or len(password) == 0 or len(email_username) == 0:
        messagebox.showwarning(
            title="Missing Credentials", message="Please fill all Fields"
        )
    else:
        try:
            with open("credentials.json", "r") as credentials:
                json_data = json.load(credentials)
        except FileNotFoundError:
            with open("credentials.json", "w") as credentials:
                json.dump(data_dict, credentials, indent=4)
        else:
            json_data.update(data_dict)

            with open("credentials.json", "w") as credentials:
                json.dump(json_data, credentials, indent=4)
        finally:
            website_entry.delete(0, END)
            email_user_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND CREDENTIALS ------------------------------- #


def find_credentials():
    website = website_entry.get()
    try:
        with open("credentials.json") as credentials:
            json_data = json.load(credentials)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Data File Found")

    else:
        if website in json_data:
            email_username = json_data[website]["email/username"]
            password = json_data[website]["password"]
            messagebox.showinfo(
                title=website,
                message=f"Email/Username:{email_username}\n Password:{password}",
            )
        else:
            messagebox.showwarning(
                title="Error", message=f"No credentials found for {website}"
            )


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# Canvas
lock_image = PhotoImage(file="logo.png")
img_canvas = Canvas(width=200, height=200)
img_canvas.create_image(100, 100, image=lock_image)
img_canvas.grid(row=0, column=1)

# Labels

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)


email_user_label = Label(text="Email/Username:")
email_user_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_user_entry = Entry(width=38)
email_user_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons

credential_search_btn = Button(text="Search", width=13, command=find_credentials)
credential_search_btn.grid(row=1, column=2)

password_gen_btn = Button(text="Generate Password", command=password_entry_generation)
password_gen_btn.grid(row=3, column=2)

add_btn = Button(text="Add", width=36, command=save_credentials)
add_btn.grid(row=4, column=1, columnspan=2)

window.mainloop()
