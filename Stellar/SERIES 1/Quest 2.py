import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair.public_key)

dummy = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy.public_key})

transaction = stellar_sdk.TransactionBuilder(
        source_account=account
    ).append_payment_op(
        destination=dummy.public_key,
        amount="10"
    ).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
