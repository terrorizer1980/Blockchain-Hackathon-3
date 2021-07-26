from Stellar.util.functions import delete_account, create_account
from Stellar.util.store_keys import SQKeypair
from stellar_sdk.exceptions import NotFoundError

if __name__ == "__main__":
    try:
        delete_account(SQKeypair)
    except NotFoundError:
        create_account(SQKeypair, 1000)
