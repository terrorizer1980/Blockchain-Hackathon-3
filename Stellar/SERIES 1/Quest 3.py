import stellar_sdk

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair.public_key)

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
).append_manage_data_op(
    data_name="Hello",
    data_value="World"
).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
