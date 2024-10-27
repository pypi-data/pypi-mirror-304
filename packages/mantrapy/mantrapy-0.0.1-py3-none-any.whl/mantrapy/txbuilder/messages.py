import json

from google.protobuf.json_format import Parse

from mantrapy.proto.cosmos.bank.v1beta1.tx_pb2 import MsgSend


def generate_bank_send_msg(sender: str, to: str, amount: str, denom: str):
    raw_msg = {
        'fromAddress': sender,
        'toAddress': to,
        'amount': [{
            'denom': denom,
            'amount': amount,
        }],
    }
    return Parse(json.dumps(raw_msg), MsgSend()) # noqa
