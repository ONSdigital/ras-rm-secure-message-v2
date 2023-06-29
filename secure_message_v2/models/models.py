from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Thread(Base):
    __tablename__ = "thread"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    subject: Mapped[str]
    category: Mapped[str]
    is_closed: Mapped[Optional[bool]]
    closed_by_id: Mapped[Optional[UUID]]
    closed_at: Mapped[Optional[datetime]]
    case_id: Mapped[Optional[UUID]]
    ru_ref: Mapped[Optional[str]]
    survey_id: Mapped[Optional[UUID]]
    assigned_internal_user_id: Mapped[Optional[UUID]]
    respondent_id: Mapped[Optional[UUID]]
    is_read_by_respondent: Mapped[bool]
    is_read_by_internal: Mapped[bool]

    messages: Mapped[List["Message"]] = relationship(back_populates="thread", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "message"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    thread_id: Mapped[UUID] = mapped_column(ForeignKey("thread.id"))
    body: Mapped[str]
    sent_at: Mapped[Optional[datetime]]
    is_from_internal: Mapped[bool]
    sent_by: Mapped[UUID]

    thread: Mapped["Thread"] = relationship(back_populates="messages")

    def to_response_dict(self):
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "body": self.body,
            "sent_at": self.sent_at,
            "is_from_internal": self.is_from_internal,
            "sent_by": self.sent_by,
        }
