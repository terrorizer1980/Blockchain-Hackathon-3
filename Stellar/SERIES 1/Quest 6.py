import stellar_sdk
import requests

server = stellar_sdk.Server()


def get_asset(code):
    try:
        issuer = server.assets().for_code("SKYECOIN").call()["_embedded"]["records"][0]["asset_issuer"]
        return stellar_sdk.Asset(code, issuer)
    except (IndexError, KeyError):
        return None


SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair.public_key)

dummy = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy.public_key})

asset = get_asset(input("Asset code: "))
XLM = stellar_sdk.Asset.native()
p = stellar_sdk.Price(10, 10)

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
).append_create_passive_sell_offer_op(
    asset.code, asset.issuer, XLM.code, XLM.issuer, "10", "10"
).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
