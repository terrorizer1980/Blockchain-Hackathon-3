import stellar_sdk
import requests
from hashlib import sha256

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))

dummies = []

for i in range(5):
    dummy = stellar_sdk.Keypair.random()
    requests.get("https://friendbot.stellar.org", params={"addr": dummy.public_key})
    dummies.append(dummy)


dummy_account = server.load_account(dummies[0].public_key)  # Gets the account from the Stellar server

memo = stellar_sdk.HashMemo(sha256(b"Stellar Quest Series 2").hexdigest())

transaction = stellar_sdk.TransactionBuilder(
    source_account=dummy_account
)

for dummy in dummies[1:]:
    transaction.append_payment_op(
        source=dummy.public_key,
        destination=dummies[0].public_key,
        amount="1000"
    )

transaction = transaction.build()

for dummy in dummies:
    transaction.sign(dummy)

server.submit_transaction(transaction)

transaction = stellar_sdk.TransactionBuilder(
        source_account=dummy_account
    ).append_create_account_op(
        destination=SQKeypair.public_key,
        starting_balance="5000"
    ).add_memo(memo).build()
transaction.sign(dummies[0])

resp = server.submit_transaction(transaction)
print(resp)
