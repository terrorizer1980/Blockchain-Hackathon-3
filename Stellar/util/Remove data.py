import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Stellar Quest Secret: "))
account = server.load_account(SQKeypair.public_key)

resp = requests.get(f"https://horizon-testnet.stellar.org/accounts/{SQKeypair.public_key}").json()

transaction = stellar_sdk.TransactionBuilder(source_account=account)

for key in resp["data"].keys():
    transaction.append_manage_data_op(
        key, None
    )

if transaction.operations:
    transaction = transaction.build()
    transaction.sign(SQKeypair)

    resp = server.submit_transaction(transaction)
    print(resp)
else:
    print("No data to remove")
