import requests
from rentalSystem.settings import API
from .strings import OVERDUE_MESSAGE

def overdue_message_formatter(info):
    renter = info[0]
    chat_id = info[1]
    balance = info[2]

    message = OVERDUE_MESSAGE.format(renter = renter, balance=balance)

    send_message(chat_id, message)

def send_message (chat_id, message):
    url_req = "https://api.telegram.org/bot" + API + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + message + "&parse_mode=HTML" 
    requests.get(url_req)    