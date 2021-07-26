from Stellar.util.functions import create_dummy_account, pay_account
from Stellar.util.store_keys import SQKeypair
from decimal import Decimal

if __name__ == '__main__':
    dummy = create_dummy_account()
    pay_account(SQKeypair, dummy, Decimal(10))
