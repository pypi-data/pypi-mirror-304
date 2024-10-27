"""Utilities module."""

DEVPIPE = {}


# Initialization


def _init_devpipe() -> None:
    """Initialize devpipe."""
    from ..database import _get_engine, create_tables
    from ..storage import _get_storage

    if DEVPIPE.get("initialized"):
        return

    _get_storage()
    _get_engine()
    create_tables()

    DEVPIPE["initialized"] = True


__all__ = ["_init_devpipe"]
