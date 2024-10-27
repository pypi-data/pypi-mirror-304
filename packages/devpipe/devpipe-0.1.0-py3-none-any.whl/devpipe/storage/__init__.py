"""Storage module.

Modules:
    local: Local storage client.
"""

import logging
from typing import Optional, Protocol

from . import local

logger = logging.getLogger(__name__)

DEVPIPE = {}


class Storage(Protocol):
    """Storage client protocol."""

    def read(self, storage_key: str) -> bytes:
        """Read data from storage.

        Args:
            storage_key (str): Storage key.

        Returns:
            Stored data.
        """

    def save(self, storage_key: str, data: bytes) -> None:
        """Save data to storage.

        Args:
            storage_key (str): Storage key.
            data (bytes): Data to store.
        """


def set_storage(storage: Optional[Storage] = None) -> Storage:
    """Set storage client.

    Args:
        storage (Optional[Storage], optional): Storage client. If not
            provided, a local storage client will be used.

    Example:
        ```python
        import devpipe as dp
        from devpipe.storage import set_storage
        from devpipe.storage.local import LocalStorage

        storage = LocalStorage()
        set_storage(storage)

        @dp.pipeline
        def my_pipeline():
            ...
        ```
    """
    if storage is None:
        storage = local.LocalStorage()
    DEVPIPE["storage"] = storage
    logger.debug(f"Storage set to `{storage.__class__.__name__}`.")
    return DEVPIPE["storage"]


def _get_storage() -> Storage:
    """Get storage client.

    Returns:
        Current storage client.
    """
    return DEVPIPE.get("storage") or set_storage()


__all__ = [
    "LocalStorage",
    "set_storage",
    "_get_storage",
]
