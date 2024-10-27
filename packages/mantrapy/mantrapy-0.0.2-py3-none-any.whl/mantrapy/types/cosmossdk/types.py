from dataclasses import dataclass
from typing import Generic
from typing import Optional
from typing import TypeVar

T = TypeVar('T')


SUCCESS_CODE = [
    200,
    201,
    202,
]


@dataclass
class QueryResponse(Generic[T]):
    """
    Generic response returned by the client to the caller of the request.
    """

    data: Optional[T] = None
    error: Optional[str] = None
    status_code: Optional[int] = None

    def is_success(self) -> bool:
        """
        Return true if the request completes successfully.
        """
        return self.error is None and self.status_code in SUCCESS_CODE
