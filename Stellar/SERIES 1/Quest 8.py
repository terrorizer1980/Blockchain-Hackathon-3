import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair)

LMX = stellar_sdk.Asset.native()
SRT = stellar_sdk.Asset("SRT", "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B")

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
).append_path_payment_strict_receive_op(
    destination=SRT.issuer,
    send_code=LMX.code,
    send_issuer=LMX.issuer,
    send_max="10",
    dest_code=SRT.code,
    dest_issuer=SRT.issuer,
    dest_amount="10",
    path=[]
).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
