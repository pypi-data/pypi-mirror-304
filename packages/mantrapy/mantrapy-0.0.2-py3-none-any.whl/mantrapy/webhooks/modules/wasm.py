from mantrapy.webhooks.modules.utils import _get_module_events


def get_wasm_events(events):
    return _get_module_events('wasm', events)
