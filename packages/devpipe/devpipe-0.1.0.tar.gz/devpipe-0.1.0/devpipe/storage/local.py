"""Local storage module."""

from ..config import CONFIG


class LocalStorage:
    """Local storage client."""

    def __init__(self):  # noqa: D107
        CONFIG.working_dir.mkdir(parents=True, exist_ok=True)
        gitignore = CONFIG.working_dir / ".gitignore"
        if not gitignore.exists():
            with open(gitignore, "w") as f:
                f.write("*")

    def read(self, storage_key: str) -> bytes:
        """Read data from storage.

        Args:
            storage_key (str): Storage key.

        Returns:
            Stored data.
        """
        filename = CONFIG.working_dir / storage_key
        with open(filename, "rb") as f:
            return f.read()

    def save(self, storage_key: str, data: bytes) -> None:
        """Save data to storage.

        Args:
            storage_key (str): Storage key.
            data (bytes): Data to store.
        """
        filename = CONFIG.working_dir / storage_key
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "wb") as f:
            f.write(data)


__all__ = ["LocalStorage"]
