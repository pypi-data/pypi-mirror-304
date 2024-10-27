from mantrapy.webhooks.modules.utils import _get_module_events


def get_distribution_events(events):
    return _get_module_events('distribution', events)
