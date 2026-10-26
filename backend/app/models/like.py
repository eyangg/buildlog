from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.time import utcnow


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        CheckConstraint(
            "(study_record_id IS NULL) <> (error_record_id IS NULL)",
            name="ck_like_one_target",
        ),
        UniqueConstraint("user_id", "study_record_id", name="uq_like_user_study_record"),
        UniqueConstraint("user_id", "error_record_id", name="uq_like_user_error_record"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    study_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("study_records.id", ondelete="CASCADE"), nullable=True
    )
    error_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("error_records.id", ondelete="CASCADE"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
