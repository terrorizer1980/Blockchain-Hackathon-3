import stellar_sdk
import requests
from hashlib import sha256

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))

dummy = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy.public_key})


dummy_account = server.load_account(dummy.public_key)  # Gets the account from the Stellar server

memo = stellar_sdk.HashMemo(sha256(b"Stellar Quest Series 2").hexdigest())

transaction = stellar_sdk.TransactionBuilder(
        source_account=dummy_account
    ).append_create_account_op(
        destination=SQKeypair.public_key,
        starting_balance="5000"
    ).add_memo(memo).build()
transaction.sign(dummy)

resp = server.submit_transaction(transaction)
print(resp)
