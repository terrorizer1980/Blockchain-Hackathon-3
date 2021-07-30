import stellar_sdk

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair)

dummy = stellar_sdk.Keypair.random()

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
).append_begin_sponsoring_future_reserves_op(
    sponsored_id=dummy.public_key
).append_create_account_op(
    destination=dummy.public_key,
    starting_balance="1"
).append_end_sponsoring_future_reserves_op(
    source=dummy.public_key
).build()
transaction.sign(SQKeypair)
transaction.sign(dummy)

resp = server.submit_transaction(transaction)
print(resp)
