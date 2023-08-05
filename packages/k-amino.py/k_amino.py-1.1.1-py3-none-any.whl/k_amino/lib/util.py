from time import time as timestamp
from typing import Dict, List
import base64
import hashlib
import hmac
from uuid import uuid4


# tapjoy = "https://ads.tapdaq.com/v4/analytics/reward"
webApi = "https://aminoapps.com/api{}".format
api = "https://service.aminoapps.com/api/v1{}".format


def generateSig(data: str):
    return base64.b64encode(
        bytes.fromhex("19") + hmac.new(bytes.fromhex("dfa5ed192dda6e88a12fe12130dc6206b1251e44"),
        data.encode(),
        hashlib.sha1).digest()
    ).decode()

def generateDevice():
    data = uuid4().bytes
    return (
        "19" + data.hex() +
        hmac.new(bytes.fromhex("e7309ecc0953c6fa60005b2765f99dbbc965c8e9"),
        bytes.fromhex("19") + data,
        hashlib.sha1).hexdigest()
        ).upper()

def uuidString():
    return str(uuid4())


def active_time(seconds=0, minutes=5, hours=0) -> List[Dict[str, int]]:
    total = seconds + minutes*60 + hours*60*60
    return [
        {
            'start': int(timestamp()),
            'end': int(timestamp() + 300)
        } for _ in range(total // 300)
    ] + [
        {
            'start': int(timestamp()),
            'end': int(timestamp() + total % 300)
        }
    ]
