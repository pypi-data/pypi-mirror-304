from mantrapy.webhooks.modules.utils import _get_module_events


def get_token_factory_events(events):
    return _get_module_events('tokenfactory', events)
