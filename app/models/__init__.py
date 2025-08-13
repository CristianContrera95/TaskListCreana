from datetime import UTC, datetime
from uuid import UUID

from sqlmodel import Field as SQLField
from sqlmodel import SQLModel


def current_utc_time():
    """Return current UTC timestamp.

    Returns:
        datetime: Current time in UTC timezone
    """
    return datetime.now(UTC)


class BaseSQLModel(SQLModel):
    created_at: datetime = SQLField(
        default_factory=current_utc_time,
        description="Timestamp when the record was created",
    )

    created_by: UUID | None = SQLField(
        default=None,
        description="ID of user who created the record",
        nullable=True,
        foreign_key="users.id",
        ondelete="SET NULL",
    )

    updated_at: datetime = SQLField(
        default_factory=current_utc_time,
        sa_column_kwargs={"onupdate": current_utc_time},
        description="Timestamp of the most recent update",
    )

    updated_by: UUID | None = SQLField(
        default=None,
        description="ID of user who last updated the record",
        nullable=True,
        foreign_key="users.id",
        ondelete="SET NULL",
    )
