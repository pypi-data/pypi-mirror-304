from dataclasses import dataclass


@dataclass
class SyncInfo:
    latest_block_hash: str
    latest_app_hash: str
    latest_block_height: str
    latest_block_time: str
    earliest_block_hash: str
    earliest_app_hash: str
    earliest_block_height: str
    earliest_block_time: str
    catching_up: bool

    # TODO: check the time thing
    @classmethod
    def from_dict(cls, data: dict) -> 'SyncInfo':
        sync_info_data = data['result']['sync_info']
        return cls(
            latest_block_hash=sync_info_data['latest_block_hash'],
            latest_app_hash=sync_info_data['latest_app_hash'],
            latest_block_height=sync_info_data['latest_block_height'],
            latest_block_time=sync_info_data['latest_block_time'],
            earliest_block_hash=sync_info_data['earliest_block_hash'],
            earliest_app_hash=sync_info_data['earliest_app_hash'],
            earliest_block_height=sync_info_data['earliest_block_height'],
            earliest_block_time=sync_info_data['earliest_block_time'],
            catching_up=sync_info_data['catching_up'],
        )
