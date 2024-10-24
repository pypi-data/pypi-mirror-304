from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models.base import Base
from fr_db.models.mixins import UUIDTimeStampMixin


class Gate(Base, UUIDTimeStampMixin):

    __table_args__ = ({'schema': 'tenant'},)

    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))

    department_id: orm.Mapped[UUID | None] = orm.mapped_column(sa.ForeignKey('tenant.department.id'))
    department: orm.Mapped["Department"] = orm.relationship(back_populates="gates", lazy="noload")

    recognitions: orm.Mapped[list["Recognition"]] = orm.relationship(back_populates="gate", lazy="noload")

    user_id: orm.Mapped[UUID] = orm.mapped_column(sa.ForeignKey('shared.gate_user.id', ondelete='CASCADE'), unique=True)
    user: orm.Mapped["GateUser"] = orm.relationship(back_populates='gate', lazy="noload")
