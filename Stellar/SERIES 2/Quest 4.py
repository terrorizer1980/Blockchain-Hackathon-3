import stellar_sdk

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Secret: "))
account = server.load_account(SQKeypair)

canClaim = stellar_sdk.ClaimPredicate.predicate_not(stellar_sdk.ClaimPredicate.predicate_before_relative_time(60*5))

claimableBalanceEntry = stellar_sdk.CreateClaimableBalance(
    asset=stellar_sdk.Asset.native(),
    amount="100",
    claimants=[stellar_sdk.Claimant(SQKeypair.public_key, canClaim)]
)

transaction = stellar_sdk.TransactionBuilder(
    source_account=account
).append_operation(
    operation=claimableBalanceEntry
).build()
transaction.sign(SQKeypair)

resp = server.submit_transaction(transaction)
print(resp)
