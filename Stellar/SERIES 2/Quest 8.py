import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair)

domain = input("Domain: ")
resp = requests.get(f"https://{domain}/.well-known/stellar.toml")
if not resp.status_code == 200:
    print("Invalid domain")
    exit()

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
).append_set_options_op(
    home_domain=domain
).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
