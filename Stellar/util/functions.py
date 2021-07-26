import requests
from decimal import Decimal
from Stellar.util.vars import *


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


def pay_account(source: stellar_sdk.Keypair, destination: stellar_sdk.Keypair, amount: Decimal, signers=[]):
    source_account = server.load_account(source.public_key)
    transaction = stellar_sdk.TransactionBuilder(
        source_account=source_account
    ).append_payment_op(
        destination=destination.public_key,
        amount=amount
    ).set_timeout(30).build()
    transaction.sign(source)
    for signer in signers:
        transaction.sign(signer)

    resp = server.submit_transaction(transaction)
    print(resp)


def store_data(source, key, value, signers=[]):
    source_account = server.load_account(source)
    transaction = stellar_sdk.TransactionBuilder(
        source_account=source_account
    ).append_manage_data_op(
        data_name=key,
        data_value=value
    ).set_timeout(30).build()
    transaction.sign(source)
    for signer in signers:
        transaction.sign(signer)

    resp = server.submit_transaction(transaction)
    print(resp)


def add_signer(source: stellar_sdk.Keypair):
    source_account = server.load_account(source.public_key)

    secondary_keypair = create_dummy_account()
    secondary_signer = stellar_sdk.Signer.ed25519_public_key(
        account_id=secondary_keypair.public_key,
        weight=1
    )

    transaction = stellar_sdk.TransactionBuilder(
        source_account=source_account
    ).append_set_options_op(
        signer=secondary_signer
    ).set_timeout(30).build()
    transaction.sign(source)

    resp = server.submit_transaction(transaction)
    print(resp)
    print(f"Signer\n------\nPublic: {secondary_keypair.public_key}\nSecret: {secondary_keypair.secret}")
    return secondary_keypair
