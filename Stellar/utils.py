import stellar_sdk
import requests
import os

from decimal import Decimal

# Stellar Quest Keys
sqk_public = os.environ.get("SQKPUBLIC") or input("Public Key: ")
sqk_secret = os.environ.get("SQKSECRET") or input("Private Key: ")
SQKeypair = stellar_sdk.Keypair.from_secret(sqk_secret)





