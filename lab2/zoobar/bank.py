from zoodb import *
from debug import *

import time
import auth_client

def init(username):
    bankdb = bank_setup()
    if bankdb.query(Bank).get(username):
        raise ValueError()

    newbank = Bank()
    newbank.username = username
    bankdb.add(newbank)
    bankdb.commit()

def transfer(sender, recipient, zoobars, token):
    if not auth_client.check_token(sender, token):
        raise ValueError()
        
    bankdb = bank_setup()
    senderp = bankdb.query(Bank).get(sender)
    recipientp = bankdb.query(Bank).get(recipient)

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankdb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    db = bank_setup()
    item = db.query(Bank).get(username)
    return item.zoobars

def get_log(username):
    db = transfer_setup()
    rows = db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username)).all()
    return [row.as_dict() for row in rows]

