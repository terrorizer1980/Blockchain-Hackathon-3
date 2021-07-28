import stellar_sdk

signers = []

while True:
    print(f"Signers: {signers}\n\n")
    print("Enter `done` to stop adding signers")
    pk = input("Signer public key: ")
    if pk.lower() == "done": break
    if pk.lower() == "rm":
        signers.pop()
        continue
    signers.append(pk)


server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Stellar Quest Secret: "))
account = server.load_account(SQKeypair.public_key)

transaction = stellar_sdk.TransactionBuilder(source_account=account)

for signer in signers:
    transaction.append_set_options_op(
        signer=stellar_sdk.Signer.ed25519_public_key(signer, 0)
    )
transaction = transaction.build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
# print(f"Signer\n------\nPublic: {signer_keypair.public_key}\nSecret: {signer_keypair.secret}")