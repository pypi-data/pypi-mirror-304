import sqlalchemy as sa
import sqlalchemy.orm as orm
from uuid import UUID

from fr_db.models import Vectorizeable


class Photo(Vectorizeable):


    __table_args__ = (
        {'schema': 'tenant'},
    )

    id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("tenant.vectorizeable.id"), primary_key=True)
    avatar: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    employee_id: orm.Mapped[UUID] = orm.mapped_column(sa.ForeignKey("tenant.employee.id", ondelete='CASCADE'), index=True)
    employee: orm.Mapped["Employee"] = orm.relationship(back_populates="photos", lazy="noload")

    __mapper_args__ = {
        'polymorphic_identity': 'Photo'
    }

