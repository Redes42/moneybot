#from __future__ import annotations

from sqlalchemy import String, ForeignKey, UniqueConstraint, Numeric, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base


class DBUser(Base):
    __tablename__ = 'users'

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    is_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=false()
    )
    persons: Mapped[list['DBPerson']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )


class DBPerson(Base):
    __tablename__ = 'persons'
    __table_args__ = (
        UniqueConstraint('chat_id', 'name', name='uq_persons_chat_id_name'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    coeff: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False, default=1.0)
    chat_id: Mapped[int] = mapped_column(
        ForeignKey('users.chat_id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    user: Mapped['DBUser'] = relationship(back_populates='persons')