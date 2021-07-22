import stellar_sdk
import requests
import os

from stellar_sdk.exceptions import NotFoundError
from decimal import Decimal

# Stellar Quest Keys
sqk_public = os.environ.get("SQKPUBLIC") or input("Public Key: ")
sqk_secret = os.environ.get("SQKSECRET") or input("Private Key")
SQKeypair = stellar_sdk.Keypair.from_secret(sqk_secret)

# FriendBot url (To create test accounts with a starting balance)
friendBot = "https://friendbot.stellar.org"

# Connect to Stellar server
testnet = "https://horizon-testnet.stellar.org/"
server = stellar_sdk.Server()


def create_dummy_account():
    keypair = stellar_sdk.Keypair.random()
    requests.get(friendBot, params={"addr": keypair.public_key})
    return keypair


def create_account(source: stellar_sdk.Keypair, amount=100):
    dummy = create_dummy_account()  # Creates an account with a balance of 10 000
    dummy_account = server.load_account(dummy.public_key)  # Gets the account from the Stellar server
    transaction = stellar_sdk.TransactionBuilder(
        source_account=dummy_account
    ).append_create_account_op(
        destination=source.public_key,
        starting_balance=Decimal(amount)
    ).set_timeout(60).build()
    transaction.sign(dummy)
    
    resp = server.submit_transaction(transaction)
    print(resp)


def delete_account(source: stellar_sdk.Keypair):  # Deletes account (In case t hasn't been set up correctly)
    destination = create_dummy_account()
    source_account = server.load_account(source.public_key)
    transaction = stellar_sdk.TransactionBuilder(
        source_account=source_account
    ).append_account_merge_op(
        destination=destination.public_key,
        source=source.public_key
    ).set_timeout(30).build()
    transaction.sign(source)

    resp = server.submit_transaction(transaction)
    print(resp)


if __name__ == "__main__":
    try:
        delete_account(SQKeypair)
    except NotFoundError:
        create_account(SQKeypair, 1000)
