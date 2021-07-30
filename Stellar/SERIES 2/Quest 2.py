import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair.public_key)

dummy = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy.public_key})
dummy_account = server.load_account(dummy.public_key)

asset_code = input("Asset code: ")
asset = stellar_sdk.Asset(asset_code, dummy.public_key)

transaction = stellar_sdk.TransactionBuilder(
    source_account=dummy_account
).append_change_trust_op(
    source=SQKeypair.public_key,
    asset_code=asset.code,
    asset_issuer=asset.issuer
).append_payment_op(
    source=asset.issuer,
    destination=SQKeypair.public_key,
    amount="1000",
    asset_code=asset.code,
    asset_issuer=asset.issuer
).build()
transaction.sign(SQKeypair)
transaction.sign(dummy)

resp = server.submit_transaction(transaction)
print(resp)
