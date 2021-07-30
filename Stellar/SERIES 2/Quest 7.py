import stellar_sdk

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair)

all_sponsored = server.accounts().for_sponsor(SQKeypair.public_key).call()["_embedded"]["records"]

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
)

for sponsored in all_sponsored:
    transaction.append_revoke_account_sponsorship_op(
        sponsored["id"]
    )

transaction = transaction.build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
