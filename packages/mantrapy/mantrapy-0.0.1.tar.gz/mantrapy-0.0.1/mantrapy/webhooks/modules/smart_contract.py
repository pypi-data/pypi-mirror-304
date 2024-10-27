from mantrapy.webhooks.modules.utils import get_events_by_type
from mantrapy.webhooks.modules.utils import get_events_by_value


def get_smart_contracts_events(events):
    # CosmWasm contracts calls are recorded in a 'wasm' event type
    return get_events_by_type('wasm', events)


def get_smart_contract_events(contract_addr, events):
    # CosmWasm contracts calls are recorded in a 'wasm' event type
    sc_events = get_smart_contracts_events(events)
    return get_events_by_value(contract_addr, sc_events)
