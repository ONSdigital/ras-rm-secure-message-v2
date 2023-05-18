from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Thread(Base):
    __tablename__ = "thread"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    subject: Mapped[str]
    category: Mapped[str]
    is_closed: Mapped[Optional[bool]]
    closed_by_id: Mapped[Optional[UUID]]
    closed_at: Mapped[Optional[DateTime]]
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

    id: Mapped[UUID] = mapped_column(primary_key=True)
    thread_id: Mapped[UUID] = mapped_column(ForeignKey("thread.id"))
    body: Mapped[str]
    sent_at: Mapped[Optional[DateTime]]
    is_from_internal: Mapped[bool]
    sent_by: Mapped[UUID]

    thread: Mapped["Thread"] = relationship(back_populates="messages")
