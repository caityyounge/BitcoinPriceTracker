from tkinter import *
from apikey import api_key
import requests
from datetime import datetime

root = Tk()
root.title('Bitcoin Price Tracker')
root.geometry('550x210')
root.config(bg='black')

previous = False

# Create a Frame
my_frame = Frame(root, bg='black')
my_frame.pack(pady=20)

# Define logo image
logo = PhotoImage(file='./bitcoin.png')
logo_label = Label(my_frame, image=logo, bg='black', bd=0)
logo_label.grid(row=0, column=0, padx=20, rowspan=2)

# Add bitcoin price label
bit_label = Label(my_frame, text='TEST',
                  font=('Helvetica', 45),
                  bg='black',
                  fg='green',
                  bd=0)
bit_label.grid(row=0, column=1, sticky="s")

# Latest Price Up/Down
latest_price = Label(my_frame, text='move test', font=('Helvetica', 10),
                     bg='black',
                     fg='grey',
                     bd=0)
latest_price.grid(row=1, column=1, sticky='n')

# Get Current Time
now = datetime.now()
current_time = now.strftime("%I:%M:%S %p")

# Create status bar
status_bar = Label(root, text=f'Last Updated {current_time}  ',
                   bd=0,
                   anchor=E,
                   bg="black",
                   fg="grey")

status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Grab the bitcoin
def update():
    global previous

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {
        'start': '1',
        'limit': '1',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, params=parameters, headers=headers)
    response_json = response.json()

    coins = response_json['data']

    price = 0
    for x in coins:
        price = x['quote']['USD']['price']

    # Update bitcoin label every 30 secs
    bit_label.config(text=f'${round(price, 2)}')
    root.after(30000, update)

    # Determine Price Change
    # Grab current price
    current = price

    if previous:
        if float(previous) > float(current):
            latest_price.config(text=f'Price Down {round(float(previous) - float(current), 2)}', fg='red')
        elif float(previous) == float(current):
            latest_price.config(text='Price Unchanged', fg='grey')
        else:
            latest_price.config(text=f'Price Up {round(float(current) - float(previous), 2)}', fg='green')

    else:
        previous = current
        latest_price.config(text='Price Unchanged', fg='grey')


update()
root.mainloop()
