import stellar_sdk

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair.public_key)

signer_keypair = stellar_sdk.Keypair.random()

signer = stellar_sdk.Signer.ed25519_public_key(
    account_id=signer_keypair.public_key,
    weight=1
)

transaction = stellar_sdk.TransactionBuilder(
        source_account=account
    ).append_set_options_op(
        signer=signer
    ).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
print(f"Signer\n------\nPublic: {signer_keypair.public_key}\nSecret: {signer_keypair.secret}")

transaction = stellar_sdk.TransactionBuilder(
        source_account=account
    ).append_manage_data_op(
        data_name="Added",
        data_value="Signer"
    ).build()
transaction.sign(signer_keypair)

resp = server.submit_transaction(transaction)
print(resp)
