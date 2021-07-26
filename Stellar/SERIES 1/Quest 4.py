from Stellar.util.functions import add_secondary_signer, store_data
from Stellar.util.store_keys import SQKeypair, SQSigners, insert_signer


if __name__ == '__main__':
    signer = add_secondary_signer(SQKeypair)
    insert_signer(signer)
    store_data(SQKeypair, "Test", "Signer", SQSigners)
