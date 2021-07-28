import requests
import stellar_sdk

server = stellar_sdk.Server()
SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair)

XLM = stellar_sdk.Asset.native()

offers = requests.get(f"https://horizon-testnet.stellar.org/accounts/{SQKeypair.public_key}/offers").json()["_embedded"]["records"]

transaction = stellar_sdk.TransactionBuilder(
    account
)

for offer in offers:
    print(offer)
    transaction.append_manage_buy_offer_op(
        *(
            (offer["selling"]["asset_code"], offer["selling"]["asset_issuer"])
            if offer["selling"]["asset_type"] != "native"
            else (XLM.code, XLM.issuer)
        ),
        *(
            (offer["buying"]["asset_code"], offer["buying"]["asset_issuer"])
            if offer["buying"]["asset_type"] != "native"
            else (XLM.code, XLM.issuer)
        ),
        "0",
        "1",
        int(offer["id"])
    )

if len(transaction.operations):
    transaction = transaction.build()
    transaction.sign(SQKeypair)
    server.submit_transaction(transaction)
else:
    print("All offers removed")
