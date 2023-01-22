from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import socket, struct
from netaddr import *
from sys import platform
import netifaces
import zxcvbn


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
current_password = {}
website = ""
email = ""
current_widgets = []


def generate_password(cur_password_entry):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_symbols + password_numbers + password_letters
    random.shuffle(password_list)

    password = ''.join(password_list)

    cur_password_entry.delete(0,END)
    cur_password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def search_password(cur_website, cur_email, current_password):
    website = cur_website
    email = cur_email
    password = current_password
    user_search = website
    try:
        with open("passwords.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="You have no saved passwords. Please save a password first.")
    else:
            if user_search in data:
                messagebox.showinfo(title=f"{user_search}", message=f"Email: {email}\nPassword: {data[user_search]['password']}")
            else:
                messagebox.showinfo(title="Error", message="No details for this website exist. You can save this website/password by adding a password and pressing 'Add'.")


def save_password(cur_website,cur_email,cur_password):
    # global website
    # global email
    # global current_password

    is_empty = False
    # website = website_entry.get()
    # email = email_entry.get()
    # current_password['password'] = password_entry.get()
    # password = password_entry.get()
    current_password['password'] = cur_password
    new_data = {cur_website: {
        "email": cur_email,
        "password": cur_password
    }

    }

    if len(cur_website) == 0 or len(cur_password) == 0:
        messagebox.showinfo(title="Oopsie", message="Please don't leave any field empty!")
        is_empty = True


    if is_empty == False:
        try:
            with open("passwords.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("passwords.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)

            with open("passwords.json", mode="w") as file:
                json.dump(data, file, indent=4)


        clear_frame()
        password_strength_screen()


def save_new_custom_password(final_password):
    global website
    global email
    #password = current_password['password']
    new_data = {website: {
        "email": email,
        "password": final_password
    }

    }

    try:
        with open("passwords.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        with open("passwords.json", mode="w") as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)

        with open("passwords.json", mode="w") as file:
            json.dump(data, file, indent=4)
    homescreen()


def get_cracktime(cur_password):
    result = zxcvbn.zxcvbn(cur_password)
    return result['crack_times_seconds']['offline_fast_hashing_1e10_per_second']

def get_password_score(cur_password):
    result = zxcvbn.zxcvbn(cur_password)
    score =  result['score']

    if score == 0:
        return '😂😂😂 Your password is as secure as a cheeto in a doorframe.'
    elif score == 1:
        return '🥴🥴🥴 Poor password choice. You will get hacked.'
    elif score == 2:
        return '🙃🙃🙃 Could be a lot better.'
    elif score ==3:
        return '🔒🔒🔒 Good security.'
    else:
        return '💪💪💪 Very strong password!'
## ---------------- FUNCTIONS FOR UI ------------- ##
def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def find_WiFi_IP():

    try:

        if platform == "linux" or platform == "linux2":
            return get_default_gateway_linux()
        elif platform == "darwin":
            gateways = netifaces.gateways()
            default_gateway = gateways['default'][netifaces.AF_INET][0]
            return default_gateway
        elif platform == "win32":
            gateways = netifaces.gateways()
            default_gateway = gateways['default'][netifaces.AF_INET][0]
            return default_gateway
    except:
        return ''

def clear_frame():
    for widget in current_widgets:
        widget.destroy()
    canvas.delete('all')

# ---------------------------- UI SETUP ------------------------------- #

def Make_it_complex(password):
    import random
    lower_cases = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z']
    upper_cases = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '€', '£', '-', '_']

    complexity = {"upper_case": False, "lower_cases": False, "number": False, "symbols": False}

    password = list(password)
    padding = []
    global_dataset = []
    final_password = ''

    for i in password:
        complexity["lower_cases"] = i.islower()
        complexity["upper_case"] = i.isupper()
        complexity["number"] = i.isdigit()
        complexity["symbols"] = not i.isalnum()

    if not complexity["lower_cases"]:
        padding.append(lower_cases[random.randint(0, len(lower_cases) - 1)])
        global_dataset = global_dataset + lower_cases
    if not complexity["upper_case"]:
        padding.append(upper_cases[random.randint(0, len(upper_cases) - 1)])
        global_dataset = global_dataset + upper_cases
    if not complexity["number"]:
        padding.append(numbers[random.randint(0, len(numbers) - 1)])
        global_dataset = global_dataset + numbers
    if not complexity["symbols"]:
        padding.append(symbols[random.randint(0, len(symbols) - 1)])
        global_dataset = global_dataset + 2 * symbols

    random.shuffle(global_dataset)

    while len(password) + len(padding) < 15:
        padding.append(random.choice(global_dataset))

    random.shuffle(padding)

    if len(padding) < 3:
        new_password = padding + password
    else:
        new_password = padding[:2] + password + padding[2:]

    for i in new_password:
        final_password = str(final_password + i)

    return (final_password)

def create_new_custom_passwords(user_word_list):
    #do something to passwords argument
    # Max's function here

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_symbols + password_numbers + password_letters
    random.shuffle(password_list)

    comp_random_password = ''.join(password_list)
    new_password_list = [words_to_password(user_word_list),Make_it_complex(current_password['password']),comp_random_password]
    display_new_custom_passwords(new_password_list)


def display_new_custom_passwords(new_passwords):
    empty_row2 = Label(text='   \n     ')
    empty_row2.grid(column=0, row=12, columnspan=3)
    current_widgets.append(empty_row2)

    empty_row3 = Label(text='   \n     ')
    empty_row3.grid(column=0, row=13, columnspan=3)
    current_widgets.append(empty_row3)

    empty_row4 = Label(text='Pick one of these new safe passwords\n')
    empty_row4.grid(column=0, row=14, columnspan=4)
    current_widgets.append(empty_row4)

    new_pass1_button = Button(width=20, text=new_passwords[0], command=lambda: save_new_custom_password(new_passwords[0]))
    new_pass1_button.grid(column=0, row=15)
    current_widgets.append(new_pass1_button)

    new_pass2_button = Button(width=20, text=new_passwords[1], command=lambda: save_new_custom_password(new_passwords[1]))
    new_pass2_button.grid(column=1, row=15)
    current_widgets.append(new_pass2_button)

    new_pass3_button = Button(width=20, text=new_passwords[2], command=lambda: save_new_custom_password(new_passwords[2]))
    new_pass3_button.grid(column=2, row=15)
    current_widgets.append(new_pass3_button)

# returns a random 3 ou 4 words assembled password
def words_to_password(user_word_list):
    password = []
    words = []
    final = ''

    for w in user_word_list:
        words.append(w)

    if len(words) < 3:
        print('error')
    else:
        words_num = 4

    for i in range(words_num):
        x = random.randint(0, len(words) - 1)
        password.append(words[x])

        words.pop(x)

    for i in password:
        final = str(final + i + '-')
    return (final[:-1])

### CREATE CANVAS FOR PASSWORD STRENGTH

def get_average_password_cracktime():
    total_seconds = 0
    counter = 0

    try:
        with open("passwords.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return "NOT AVAILABLE. NO PASSWORDS SAVED"

    for key, value in data.items():
        cur_password = value['password']
        cur_cracktime = get_cracktime(cur_password)
        total_seconds += cur_cracktime
        counter += 1
    return F'Your average password crack time is {round((total_seconds / counter),2)} seconds.'

def password_strength_screen():
    global current_widgets
    clear_frame()
    password_label = Label(text="Your current password:")
    password_label.grid(column=0, row=1)
    current_widgets.append(password_label)

    curr_password = Label(text=current_password['password'])
    curr_password.grid(column=1, row=1, columnspan=2)
    current_widgets.append(curr_password)

    pass_strength_label = Label(text="Your password strength:")
    pass_strength_label.grid(column=0, row=2)
    current_widgets.append(pass_strength_label)

    pass_strength_value = Label(text=f"{get_password_score(current_password['password'])} \n")
    pass_strength_value.grid(column=1, row=2, columnspan=2)
    current_widgets.append(pass_strength_value)

    crack_speed_label = Label(text=f"A hacker can crack your password in {round(get_cracktime(current_password['password']),2)} seconds!!")
    crack_speed_label.grid(column=1, row=3, columnspan=2)
    current_widgets.append(crack_speed_label)


    empty_row1 = Label(text='   \n     ')
    empty_row1.grid(column=0, row=4, columnspan=4)
    current_widgets.append(empty_row1)

    empty_row1 = Label(text='   \n     ')
    empty_row1.grid(column=0, row=5, columnspan=4)
    current_widgets.append(empty_row1)


    word1_label = Label(text='Type a new word below:')
    word1_label.grid(column=0, row=9)
    current_widgets.append(word1_label)

    word2_label = Label(text='Type a new word below:')
    word2_label.grid(column=1, row=9)
    current_widgets.append(word2_label)

    word3_label = Label(text='Type a new word below:')
    word3_label.grid(column=2, row=9)
    current_widgets.append(word3_label)

    word4_label = Label(text='Type a new word below:')
    word4_label.grid(column=3, row=9)
    current_widgets.append(word4_label)


    word1_entry = Entry(width=21)
    word1_entry.grid(column=0, row=10)
    current_widgets.append(word1_entry)

    word2_entry = Entry(width=21)
    word2_entry.grid(column=1, row=10)
    current_widgets.append(word2_entry)

    word3_entry = Entry(width=21)
    word3_entry.grid(column=2, row=10)
    current_widgets.append(word3_entry)

    word4_entry = Entry(width=21)
    word4_entry.grid(column=3, row=10)
    current_widgets.append(word4_entry)

    new_passwords_button = Button(width=40, text="Generate new passwords with my words", command=lambda: create_new_custom_passwords([word1_entry.get(),word2_entry.get(),word3_entry.get(),word4_entry.get()]))
    new_passwords_button.grid(column=1, row=11, columnspan=2)
    current_widgets.append(new_passwords_button)

    empty_row2 = Label(text='   \n     ')
    empty_row2.grid(column=0, row=17, columnspan=2)
    current_widgets.append(empty_row2)

    empty_row3 = Label(text='   \n     ')
    empty_row3.grid(column=0, row=18, columnspan=2)
    current_widgets.append(empty_row3)

    back_button = Button(text='Go Back', command=homescreen)
    back_button.grid(column=3, row=19, columnspan=1)
    current_widgets.append(back_button)


def IP_screen():
    global current_widgets
    clear_frame()
    home_ip_label = Label(text='Home IP address: ')
    home_ip_label.grid(column=0, row=1)
    current_widgets.append(home_ip_label)

    home_ip_entry = Entry(width=21)
    home_ip_entry.grid(column=1, row=1)
    home_ip_entry.insert(0,get_IP('home'))
    current_widgets.append(home_ip_entry)

    im_at_home_button = Button(text="I'm at home, find my IP.", command= lambda: [home_ip_entry.delete(0,END),home_ip_entry.insert(0, find_WiFi_IP())])
    im_at_home_button.grid(column=2, row=1)
    current_widgets.append(im_at_home_button)

    submit_home_button = Button(text="Submit home IP.", command=lambda: save_IP_address('home',home_ip_entry.get()))
    submit_home_button.grid(column=3, row=1)
    current_widgets.append(submit_home_button)

    work_ip_label = Label(text='Work IP address: ')
    work_ip_label.grid(column=0, row=2)
    current_widgets.append(work_ip_label)

    work_ip_entry = Entry(width=21)
    work_ip_entry.grid(column=1, row=2)
    work_ip_entry.insert(0,get_IP('work'))
    current_widgets.append(work_ip_entry)

    im_at_work_button = Button(text="I'm at work, find my IP.", command=lambda: [work_ip_entry.delete(0,END),work_ip_entry.insert(0, find_WiFi_IP())])
    im_at_work_button.grid(column=2, row=2)
    current_widgets.append(im_at_work_button)

    submit_work_button = Button(text="Submit work IP.", command=lambda: save_IP_address('work',work_ip_entry.get()))
    submit_work_button.grid(column=3, row=2)
    current_widgets.append(submit_work_button)



    back_button = Button(text='Go Back', command=homescreen)
    back_button.grid(column=2, row=3, columnspan=2)
    current_widgets.append(back_button)

def existing_password_strength_screen():
    clear_frame()
    pass_strength_label = Label(text=get_average_password_cracktime())
    pass_strength_label.grid(column=0, row=0, columnspan=2)
    current_widgets.append(pass_strength_label)

    back_button = Button(text='Go Back', command=homescreen)
    back_button.grid(column=0, row=1)
    current_widgets.append(back_button)

    quiz_button = Button(text='Common misconceptions/FAQs', fg='red', command=FAQ_screen)
    quiz_button.grid(column=1, row=1)
    current_widgets.append(quiz_button)


def save_IP_address(place, IP):
    new_data = {place: IP}

    try:
        with open("IP.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        with open("IP.json", mode="w") as file:
            json.dump(new_data, file, indent=4)
        with open("IP.json", mode="w") as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)

        with open("IP.json", mode="w") as file:
            json.dump(data, file, indent=4)

def get_IP(place):
    try:
        with open("IP.json", mode="r") as file:
            data = json.load(file)
            IP = data[place]
    finally:
        if len(IP) == 0:
            return ''
        else:
            return IP

def is_public_IP():
    try:
        with open("IP.json", mode="r") as file:
            data = json.load(file)
            home_IP = data['home']
    except FileNotFoundError:
        return True
    if home_IP == find_WiFi_IP():
        return False
    else:
        return True

def set_website(new_website):
    global website
    website = new_website

def set_email(new_email):
    global email
    email = new_email

def set_password(new_password):
    global current_password
    current_password['password'] = new_password

def homescreen():
    clear_frame()
    global current_widgets
    current_widgets = []

    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(column=1, row=0)

    website_label = Label(text="Website:")
    website_label.grid(column=0, row=1)
    current_widgets.append(website_label)

    email_label = Label(text="Email/Username:")
    email_label.grid(column=0, row=2)
    current_widgets.append(email_label)

    password_label = Label(text="Password:")
    password_label.grid(column=0, row=3)
    current_widgets.append(password_label)

    website_entry = Entry(width=21)
    website_entry.grid(column=1, row=1)
    website_entry.focus()
    current_widgets.append(website_entry)
    global website

    email_entry = Entry(width=35)
    email_entry.grid(column=1, row=2, columnspan=2)
    #email_entry.insert(0, "default_email@email.com")
    current_widgets.append(email_entry)
    global email

    password_entry = Entry(width=21)
    password_entry.grid(column=1, row=3)
    current_widgets.append(password_entry)
    global current_password

    generate_password_button = Button(text="Generate Password", command=lambda: generate_password(password_entry))
    generate_password_button.grid(column=2, row=3)
    current_widgets.append(generate_password_button)

    add_button = Button(width=36, text="Add", command=lambda: [set_website(website_entry.get()),set_email(email_entry.get()),set_password(password_entry.get()),save_password(website_entry.get(), email_entry.get(), password_entry.get())])
    add_button.grid(column=1, row=4, columnspan=2)
    current_widgets.append(add_button)

    search_button = Button(width=13, text="Search", command=lambda: search_password(website_entry.get(),email_entry.get(), password_entry.get()))
    search_button.grid(column=2, row=1)
    current_widgets.append(search_button)

    empty_row1 = Label(text='   \n     ')
    empty_row1.grid(column=0, row=5, columnspan=2)
    current_widgets.append(empty_row1)

    empty_row2 = Label(text='   \n     ')
    empty_row2.grid(column=0, row=6, columnspan=2)
    current_widgets.append(empty_row2)

    IP_button = Button(text='Configure Home/Work IP', command=IP_screen)
    IP_button.grid(column=2, row=7)
    current_widgets.append(IP_button)

    all_passwords_strength_button = Button(text="Cumulative strength of all passwords", command=existing_password_strength_screen)
    all_passwords_strength_button.grid(column=0, row=7)
    current_widgets.append(all_passwords_strength_button)

def FAQ_screen():
    global current_widgets
    clear_frame()
    q1_label = Label(text="Is using the name of your son’s dog called “puppy” followed by the age of your mother which is “93” a strong password? ")
    q1_label.grid(column=0, row=1)
    current_widgets.append(q1_label)

    q1_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer", message="No because it is too common. Make it complex and/or long but most importantly: unique")))
    q1_button.grid(column=1,row=1)
    current_widgets.append(q1_button)

    q2_label = Label(
        text="Which password is the strongest: Q#4*ry7\& or mummymummymummy?")
    q2_label.grid(column=0, row=2)
    current_widgets.append(q2_label)

    q2_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="First one takes 93 years for a hacker to hack and the 2nd takes 1 000 years. Password length increases strength exponentially.")))
    q2_button.grid(column=1, row=2)
    current_widgets.append(q2_button)

    q3_label = Label(
        text="Is it a good practice to use as a password your favourite sports (golf,soccer etc) and your birthday year since it is easy to rememeber it?")
    q3_label.grid(column=0, row=3)
    current_widgets.append(q3_label)

    q3_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="No because sometimes personal data like favourite sports, birthday could have been shared through a social network app thus making them public and not very safe. You could use: 19GOLF32-my'sport'")))
    q3_button.grid(column=1, row=3)
    current_widgets.append(q3_button)

    q4_label = Label(
        text="What's better practice: a) The use of many special characters b) A complex password with upper and lower cases, number and special characters c)A very long password")
    q4_label.grid(column=0, row=4)
    current_widgets.append(q4_label)

    q4_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="Using 1 or 10 special characters does not affect the strength of the password. The use of a complex password is better but increasing the length increases exponentially the strength of the password.")))
    q4_button.grid(column=1, row=4)
    current_widgets.append(q4_button)

    q5_label = Label(
        text="Is writing  “folg” rather than “golf” in your password useful?")
    q5_label.grid(column=0, row=5)
    current_widgets.append(q5_label)

    q5_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="While it does improve strength marginally, password needs to be more complex and/or long enough to increase it's strength")))
    q5_button.grid(column=1, row=5)
    current_widgets.append(q5_button)

    q6_label = Label(
        text="Using complex words from the dictionary is not a good idea")
    q6_label.grid(column=0, row=6)
    current_widgets.append(q6_label)

    q6_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="Correct. The less meaningful your password is, the better.")))
    q6_button.grid(column=1, row=6)
    current_widgets.append(q6_button)

    q7_label = Label(
        text="Using the same very complex password for every website is a good idea.")
    q7_label.grid(column=0, row=7)
    current_widgets.append(q7_label)

    q7_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="No. Try to change passwords as much as possible or at least do some proper variations to an already complex password.")))
    q7_button.grid(column=1, row=7)
    current_widgets.append(q7_button)

    q8_label = Label(
        text="Using our own complex password is better than losing time and energy to set-up and use a password manager/generator")
    q8_label.grid(column=0, row=8)
    current_widgets.append(q8_label)

    q8_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="No. Using a password manager/generator is by far the most secure technique if the passwords generated are long and complex enough. We recommend a password length of at least 15 characters with upper and lower cases, digits and special characters.")))
    q8_button.grid(column=1, row=8)
    current_widgets.append(q8_button)

    q9_label = Label(
        text="There is no way to forget my password if I use a password manager")
    q9_label.grid(column=0, row=9)
    current_widgets.append(q9_label)

    q9_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="Wrong. To access your password, you need to have a master password. If master password is lost there will be no way of using the password manager.")))
    q9_button.grid(column=1, row=9)
    current_widgets.append(q9_button)

    q10_label = Label(
        text="Having a strong password for every website except for my e-mail account, isn't that dangerous.")
    q10_label.grid(column=0, row=10)
    current_widgets.append(q10_label)

    q10_button = Button(text='See answer', command=lambda: (messagebox.showinfo(title="Answer",
                                                                               message="Wrong. If your e-mail account password leaks, the hacker will take control of your e-mail account and reset every password of every website you’re registered in so you won’t have access to them anymore.")))
    q10_button.grid(column=1, row=10)
    current_widgets.append(q10_button)

    empty_row1 = Label(text='   \n     ')
    empty_row1.grid(column=0, row=11, columnspan=2)
    current_widgets.append(empty_row1)

    empty_row2 = Label(text='   \n     ')
    empty_row2.grid(column=0, row=12, columnspan=2)
    current_widgets.append(empty_row2)

    back_button = Button(text='Go Back', command=homescreen)
    back_button.grid(column=0, row=13, columnspan=2)
    current_widgets.append(back_button)









window = Tk()
window.title("Password Manager")
window.config(width=200, height=200, padx=50, pady=50)

canvas = Canvas(width=200, height=200)

logo_img = PhotoImage(file="logo.png")
homescreen()
if is_public_IP():
    messagebox.showinfo(title="Careful",
                        message="I cannot confirm that you are on your private home/work network. You may be on an unsafe network."
                                "Avoid putting your passwords online right now.")

window.mainloop()
