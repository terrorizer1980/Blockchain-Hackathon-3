import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair.public_key)

dummy = stellar_sdk.Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": dummy.public_key})
dummy_account = server.load_account(dummy.public_key)

transaction1 = stellar_sdk.TransactionBuilder(
    source_account=account
).append_manage_data_op(
    data_name="Test",
    data_value="Data"
).build()
transaction1.sign(SQKeypair)


transaction2 = stellar_sdk.TransactionBuilder(
    source_account=account
).build_fee_bump_transaction(
    fee_source=dummy,
    base_fee=100,
    inner_transaction_envelope=transaction1.to_transaction_envelope_v1()
)
transaction2.sign(dummy)

resp = server.submit_transaction(transaction2)
print(resp)
