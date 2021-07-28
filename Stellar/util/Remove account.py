import stellar_sdk
import requests

from stellar_sdk.exceptions import NotFoundError

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))

try:
    account = server.load_account(SQKeypair.public_key)
except NotFoundError:
    print("Account doesn't exist")
    exit()


dummy = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy.public_key})


transaction = stellar_sdk.TransactionBuilder(
    account
).append_account_merge_op(
    dummy.public_key
).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
