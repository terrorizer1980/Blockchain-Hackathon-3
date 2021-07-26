from Stellar.util.functions import store_data
from Stellar.util.store_keys import SQKeypair


if __name__ == '__main__':
    store_data(SQKeypair, "Hello", "World")
