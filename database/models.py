from datetime import datetime
from typing import Any
from sqlalchemy import BigInteger, String, Integer, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class SnapshotHistory(Base):
    __tablename__ = "snapshot_history"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    data: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )    
    
class CurrentSnapshot(Base):
    __tablename__ = "current_snapshot"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    value: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )