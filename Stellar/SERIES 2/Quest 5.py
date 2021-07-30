import stellar_sdk

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair)

claimables = server.claimable_balances().for_claimant(SQKeypair.public_key).call()["_embedded"]["records"]
ids = [_["id"] for _ in claimables]

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
)
for _id in ids:
    transaction.append_claim_claimable_balance_op(
        balance_id=_id
    )
transaction = transaction.build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
