"""Password manager."""
import random
import json
import tkinter as tk
import os
from tkinter import messagebox
import pyperclip
from cryptography.fernet import Fernet


# DO IN THE FUTURE:
#   - Get list of saved websites

KEY = None

# -------------- MASTER PWD LOGIC ---------------------
try:
    MASTER_PWD = os.environ["MASTER_PWD_PASSMANAGER"]
except KeyError:
    MASTER_PWD = None
    messagebox.showinfo(message="No master password set")

# to decrypt: Fernet(KEY).decrypt(what_to_decrypt.encode()).decode()
# to encrypt: Fernet(KEY).encrypt(what_to_encrypt.encode()).decode()


def master_pass():
    """Moudle for master password."""
    def master_pass_updater():
        """Update master password in .bashrc (environment variable)."""
        if check_old_match():
            if check_new_confirm():
                # Replace old .bashrc entry
                new_master = Fernet(KEY).encrypt(
                    new_entry.get().encode()).decode()
                with open(os.path.expanduser("~/.bashrc"),
                          "r", encoding="utf8") as file:
                    # Find the right line and replace
                    data = file.read()
                    old_var = f"export MASTER_PWD_PASSMANAGER={MASTER_PWD}\n"
                    new_var = f"export MASTER_PWD_PASSMANAGER={new_master}\n"
                    data = data.replace(old_var, new_var)
                with open(os.path.expanduser("~/.bashrc"),
                          "w", encoding="utf8") as file_two:
                    file_two.write(data)
                    messagebox.showinfo(message="Password updated."
                                        "\nPlease restart the terminal!")
                    top1.destroy()
        else:
            if check_new_confirm():
                new_master = Fernet(KEY).encrypt(
                    new_entry.get().encode()).decode()
                full_command = f"export MASTER_PWD_PASSMANAGER={new_master}\n"
                with open(os.path.expanduser("~/.bashrc"),
                          "a", encoding="utf8") as file:
                    file.write(full_command)
                    messagebox.showinfo(message="Password updated.\n"
                                                "Please restart the terminal!")
                    top1.destroy()

    def check_new_confirm():
        """Confront new and confirm password."""
        if MASTER_PWD is not None:
            if new_entry.get() != confirm_entry.get():
                messagebox.showerror(title="Error in new password",
                                     message="new passwords are different.")
                return False
        # Check if needs to be false and indent the true under second if
        return True

    def check_old_match():
        """Use if MASTER_PWD is not None."""
        old_decrypted = Fernet(KEY).decrypt(MASTER_PWD.encode()).decode()
        if old_decrypted != old_entry.get():
            messagebox.showerror(title="Error in old password",
                                 message="Old password doesn't match.")
            return False
        return True

    # UI
    top1 = tk.Toplevel(window, padx=10, pady=10)
    if MASTER_PWD is not None:
        # Ask for old password, new password , confirm new
        old_label = tk.Label(top1, text="Enter old password")
        old_label.pack(pady=5)
        old_entry = tk.Entry(top1, show='*')
        old_entry.pack(pady=5)

    new_label = tk.Label(top1, text="Enter new password")
    new_label.pack(pady=5)
    new_entry = tk.Entry(top1, show='*')
    new_entry.pack(pady=5)
    confirm_label = tk.Label(top1, text="Confirm new password")
    confirm_label.pack(pady=5)
    confirm_entry = tk.Entry(top1, show='*')
    confirm_entry.pack(pady=5)

    ok_btn = tk.Button(top1, text="OK", command=master_pass_updater)
    ok_btn.pack(pady=5)

    top1.bind("<Return>", lambda event=None: ok_btn.invoke())


# -------------- ENCRYPTION KEY CREATOR -----------------

def create_key():
    """Create encryption key and save it on file."""
    global KEY
    exist = os.path.exists("my_key.key")
    if exist:
        test = messagebox.askquestion(
            title="Warning",
            message="Key file is already present.\nOverwrite?")
        if test == "yes":
            messagebox.showinfo(message="Key file overwritten")
            KEY = Fernet.generate_key()
            with open('my_key.key', 'wb') as file:
                file.write(KEY)
    else:
        KEY = Fernet.generate_key()
        with open('my_key.key', 'wb') as file:
            file.write(KEY)


def load_key():
    """Load encryption key from file."""
    global KEY
    try:
        with open('my_key.key', 'rb') as file:
            KEY = file.read()
        messagebox.showinfo(message="key loaded")
    except FileNotFoundError:
        messagebox.showerror(
            title="Error",
            message=("No key found.\n"
                     "Create one with the button in the main screen or "
                     "copy an existing one in the same folder.")
        )


# ---------------------------- SAVE PASSWORD ------------------------------- #

def data_saver():
    """Encrypt password and saves it to file."""
    if KEY is not None:
        encrypted = Fernet(KEY).encrypt(entry_pw.get().encode())

        new_data = {
            entry_website.get().upper(): {
                "email": entry_uname.get(),
                "password": encrypted.decode(),
            }
        }
        if len(
            entry_website.get()) == 0 or len(
            entry_uname.get()) == 0 or len(
                entry_pw.get()) == 0:
            messagebox.showerror(
                title='Error',
                message='Entries cannot be blank.')
        else:
            try:
                with open("pw.json", "r", encoding="utf8") as file:
                    data = json.load(file)
                    data.update(new_data)

            except (json.decoder.JSONDecodeError, FileNotFoundError) as err:
                print(f'Warning: {err}.\n'
                      f'File missing or empty, creating a new one.')
                with open("pw.json", "w", encoding="utf8") as file:
                    json.dump(new_data, file, indent=4)
            else:
                with open("pw.json", "w", encoding="utf8") as file:
                    json.dump(data, file, indent=4)
            finally:
                messagebox.showinfo(message="Password saved.")
                entry_website.delete(0, tk.END)
                entry_pw.delete(0, tk.END)
    else:
        messagebox.showerror(title="error", message="Create or load key first")


# ----------------- PASSWORD GENERATOR -------------------------- #

def pw_gen():
    """Random password generator."""
    entry_pw.delete(0, tk.END)
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = ''.join(password_list)
    pyperclip.copy(password)
    entry_pw.insert(0, password)


# ---------------------------------- SEARCH FUNCTION -----------------------

def website_search():
    """Search for specified website in JSON file."""
    if KEY is None:
        load_key()

    def pwd_checker():
        if master_entry.get() == MASTER_PWD:
            top1.destroy()
            website = entry_website.get().upper()
            top = tk.Toplevel(window, padx=20, pady=20)
            top.title(website)
            try:
                with open('pw.json', 'r', encoding="utf8") as file:
                    data = json.load(file)
            except FileNotFoundError:
                top.title("Error")
                info_label = tk.Label(top, text="No password file found.",
                                      justify=tk.CENTER,
                                      font=("Ariel", 14, 'bold'))
                info_label.pack()
            else:
                try:
                    enc_pw = Fernet(KEY).decrypt(
                        data[website]['password'].encode()).decode()
                    info_label = tk.Label(
                        top, text=f"Email: {data[website]['email']}\n"
                        f"Password: {enc_pw}", justify=tk.CENTER, font=(
                            "Ariel", 14, 'bold'))
                    info_label.pack()
                except KeyError:
                    top.title('No password found')
                    info_label = tk.Label(
                        top,
                        text="No password saved\nfor this website.",
                        justify=tk.CENTER,
                        font=(
                            "Ariel",
                            14,
                            'bold'))
                    info_label.pack()
        else:
            top1.destroy()
            messagebox.showerror(
                title="Password error",
                message="Incorrect password")

    top1 = tk.Toplevel(window, padx=10, pady=10)
    master_label = tk.Label(top1, text="Enter master password")
    master_label.pack(pady=5)
    master_entry = tk.Entry(top1, show='*')
    master_entry.pack(pady=5)
    master_entry.focus()
    master_btn = tk.Button(top1, text="Confirm", command=pwd_checker)
    master_btn.pack(pady=5)
    top1.bind("<Return>", lambda event=None: master_btn.invoke())


window = tk.Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg='white')

tag_website = tk.Label(text='Website:  ', bg='white', highlightthickness=0)
tag_website.grid(column=0, row=1)
tag_uname = tk.Label(text='Email/Username:  ', bg='white')
tag_uname.grid(column=0, row=2)
tag_pw = tk.Label(text='Password:  ', bg='white', highlightthickness=0)
tag_pw.grid(column=0, row=3)

entry_website = tk.Entry(width=28, bg='white', highlightthickness=0)
entry_website.grid(column=1, row=1, sticky='w')
entry_website.focus()

entry_uname = tk.Entry(width=48, bg='white', highlightthickness=0)
entry_uname.grid(column=1, row=2, columnspan=2, sticky='w')
entry_uname.insert(tk.END, 'test@test.com')

entry_pw = tk.Entry(width=28, bg='white', highlightthickness=0, show='*')
entry_pw.grid(column=1, row=3, sticky='w')

btn_gen_pw = tk.Button(
    text='Generate Password',
    width=16,
    bg='white',
    highlightthickness=0,
    command=pw_gen)
btn_gen_pw.grid(column=2, row=3)

btn_add = tk.Button(
    text='Add',
    width=45,
    bg='white',
    highlightthickness=0,
    command=data_saver)
btn_add.grid(column=1, row=4, columnspan=2, sticky='w')

btn_search = tk.Button(
    text='Search',
    bg='white',
    width=16,
    highlightthickness=0,
    command=website_search)
btn_search.grid(column=2, row=1)

btn_create_key = tk.Button(
    text='Create encryption Key',
    bg='white',
    width=16,
    highlightthickness=0,
    command=create_key)
btn_create_key.grid(column=0, row=0, padx=10, pady=10)

btn_load_key = tk.Button(
    text='Load encryption Key',
    bg='white',
    width=16,
    highlightthickness=0,
    command=load_key)
btn_load_key.grid(column=1, row=0, padx=10, pady=10)

btn_mpwd_key = tk.Button(
    text='Set/Change Mpwd',
    bg='white',
    width=16,
    highlightthickness=0,
    command=master_pass)
btn_mpwd_key.grid(column=2, row=0, padx=10, pady=10)


window.mainloop()
