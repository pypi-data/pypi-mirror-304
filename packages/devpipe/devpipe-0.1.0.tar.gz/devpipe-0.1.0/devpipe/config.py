"""Configuration module."""

from pathlib import Path
from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Config(BaseSettings):
    """Configuration class.

    Attributes:
        database_url (Optional[str]): Database URL. If not provided, a
            SQLite database will be created in the devpipe working
            directory. Any SQLAlchemy-compatible URL is accepted, provided
            that the required database driver is installed.
        database_prefix (str): Database tables prefix.
        working_dir (Path): devpipe working directory.

    !!! info
        Configuration is loaded from environment variables prefixed with
        `DEVPIPE_`. For example,
        `DEVPIPE_DATABASE_URL=postgresql://user:password@localhost:5432/db`.
        sets the `database_url` attribute so that devpipe uses a PostgreSQL
        database.
    """

    database_url: Optional[str] = Field(default=None)
    database_prefix: str = Field(default="devpipe")
    working_dir: Path = Field(
        default_factory=lambda: Path(".devpipe"),
    )

    model_config = SettingsConfigDict(
        env_prefix="DEVPIPE_",
    )

    @model_validator(mode="after")
    def _set_default_database_url(self) -> Self:
        if self.database_url is None:
            file = self.working_dir / ".devpipe.sqlite"
            self.database_url = f"sqlite:///{file.absolute()}"
        return self


CONFIG = Config()


__all__ = ["Config"]
