import json
from stellar_sdk import Keypair

SQKeypair = None
SQSigners = []

try:
    with open("keys.json", "r") as _f:
        _data = json.load(_f)
    SQKeypair = Keypair.from_secret(_data["secret"])
    for _signer in _data["signers"]:
        SQSigners.append(Keypair.from_secret(_signer["secret"]))
except (KeyError, FileNotFoundError, json.JSONDecodeError) as _e:
    print(_e)
    _keys = {
        "public": input("Public: "),
        "secret": input("Secret: "),
        "signers": []
    }
    with open("keys.json", "w") as _f:
        json.dump(_keys, _f, indent=4)
    SQKeypair = Keypair.from_secret(_keys["secret"])


def insert_signer(_signer: Keypair):
    with open("keys.json", "r") as _f:
        _data = json.load(_f)

    _data["signers"].append({"public": _signer.public_key, "secret": _signer.secret})

    with open("keys.json", "w") as _f:
        json.dump(_data, _f, indent=4)
