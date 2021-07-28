import stellar_sdk
import requests
import json

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Stellar Quest Secret: "))
account = server.load_account(SQKeypair.public_key)

print("* for all")
asset_code = input("Asset code: ")

resp = requests.get(f"https://horizon-testnet.stellar.org/accounts/{SQKeypair.public_key}").json()

if asset_code == "*":
    balances = [(_["asset_issuer"], _["balance"], _["asset_code"]) for _ in resp["balances"] if "asset_code" in _]
else:
    balances = [(_["asset_issuer"], _["balance"], _["asset_code"]) for _ in resp["balances"] if "asset_code" in _ and _["asset_code"] == asset_code]

print(json.dumps(resp["balances"], indent=4))

transaction = stellar_sdk.TransactionBuilder(source_account=account)

for balance in balances:
    print(balance)
    if float(balance[1]):
        transaction.append_payment_op(
            destination=balance[0], amount=balance[1], asset_code=balance[2], asset_issuer=balance[0], source=SQKeypair.public_key
        )
    transaction.append_change_trust_op(
        balance[2], balance[0], "0"
    )

if len(transaction.operations):
    transaction = transaction.build()
    transaction.sign(SQKeypair)

    resp = server.submit_transaction(transaction)
    print(resp)
else:
    print("No assets to remove")
