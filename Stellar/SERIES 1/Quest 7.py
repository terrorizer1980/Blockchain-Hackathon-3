import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))

dummy1 = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy1.public_key})
dummy1_account = server.load_account(dummy1)

dummy2 = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy2.public_key})

transaction = stellar_sdk.TransactionBuilder(
    source_account=dummy1_account
).append_payment_op(
    source=SQKeypair.public_key,
    destination=dummy2.public_key,
    amount="10"
).build()
transaction.sign(SQKeypair)
transaction.sign(dummy1)

resp = server.submit_transaction(transaction)
print(resp)
