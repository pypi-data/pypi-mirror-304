import requests
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_exponential


class EventProcessor:

    def __init__(self, webhook_url, process_event_fn, post_retries=3):
        self.webhook_url = webhook_url
        self.process_fn = process_event_fn

        self.send_notification_with_retry = retry(
            stop=stop_after_attempt(post_retries),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type(requests.exceptions.RequestException),
        )(self._send_notification)

    def set_query(self, query):
        self.query = query

    def set_hook_id(self, hook_id):
        self.hook_id = hook_id

    def process_events(self, events):
        processed_events = self.process_fn(events)
        if len(processed_events) == 0:
            return
        notification = {'events': processed_events}
        if self.query is not None:
            notification['query'] = self.query
        if self.hook_id is not None:
            notification['hook_id'] = self.hook_id
        self.send_notification_with_retry(notification)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException),
    )
    def _send_notification(self, notification):
        response = requests.post(self.webhook_url, json=notification)
        response.raise_for_status()
