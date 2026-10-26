from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.time import utcnow


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        CheckConstraint(
            "target_type IN ('study_record', 'todo_item', 'error_record', 'comment')",
            name="ck_report_target_type",
        ),
        UniqueConstraint("reporter_id", "target_type", "target_id", name="uq_report_once_per_target"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    target_type: Mapped[str] = mapped_column(String(20))
    target_id: Mapped[int]
    reason: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
