from mantrapy.webhooks.modules.utils import _get_module_events
from mantrapy.webhooks.modules.utils import get_events_by_attr_value

MSG_BANK_SEND = '/cosmos.bank.v1beta1.MsgSend'


def get_bank_events(events):
    return _get_module_events('bank', events)


def get_bank_events_for_addr(addr, events):
    _ = addr
    return _get_module_events('bank', events)


def get_bank_tranfer_events(events):
    return get_events_by_attr_value('action', MSG_BANK_SEND, events)
