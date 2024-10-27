from base64 import b64decode
from base64 import b64encode
from dataclasses import dataclass
from typing import Optional


@dataclass
class PageResponse:
    """
    PageResponse contains pagination information returned by the API.

    Attributes:
        next_key (bytes): Key to be passed to PageRequest.key to query the next page.
                         Will be empty if there are no more results.
        total (int): Total number of results available if PageRequest.count_total was set.
                    Value is undefined otherwise.
    """

    next_key: Optional[bytes] = None
    total: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary format, encoding bytes as base64 for JSON compatibility"""
        return {
            'next_key':
            b64encode(self.next_key).decode() if self.next_key else None,
            'total': self.total,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PageResponse':
        """Create PageResponse from dictionary data"""
        return cls(
            next_key=b64decode(data['next_key'])
            if data.get('next_key') else None,
            total=int(data['total']) if data.get('total') else None,
        )
