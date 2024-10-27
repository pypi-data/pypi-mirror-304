from typing import List


class Attribute:
    key: str
    value: str


class CosmosEvent:
    type: str
    attributes: List[Attribute]


def get_event(event_type, events: List[CosmosEvent]):
    for e in events:
        if e.type == event_type:
            return e


def get_events_by_type(
    event_type,
    events: List[CosmosEvent],
) -> List[CosmosEvent]:
    return [e for e in events if e['type'] == event_type]


def get_events_by_attribute(
    attr,
    events: List[CosmosEvent],
) -> List[CosmosEvent]:
    return [
        e for e in events
        if any(a['key'] == attr for a in e['attributes'])
    ]


def get_events_by_attr_value(
    attribute: str,
    attr_val: str,
    events:
    List[CosmosEvent],
) -> List[CosmosEvent]:
    return [
        e for e in events if any(
            a.get('key') == attribute and a.get('value') == attr_val
            for a in e.get('attributes', [])
        )
    ]


def get_events_by_value(
    attr_val,
    events: List[CosmosEvent],
) -> List[CosmosEvent]:
    return [
        e for e in events
        if any(a['value'] == attr_val for a in e['attributes'])
    ]


def get_event_attribute(attribute, event: CosmosEvent):
    for a in event['attributes']:
        if a.key == attribute:
            return a


def get_module_events(module, events: List[CosmosEvent]):
    return get_events_by_attr_value('module', module, events)


def get_account_events(addr, events: List[CosmosEvent]):
    return get_events_by_value(addr, events)


def only_mod_events(events: List[CosmosEvent]) -> List[CosmosEvent]:
    if events is None:
        return []
    return [
        event for event in events if isinstance(event, dict) and isinstance(
            event.get('attributes'),
            dict,
        ) and 'module' in event['attributes']
    ]


def get_account_modules_events(addr, events):
    all_events = get_account_events(addr, events)
    return only_mod_events(all_events)
