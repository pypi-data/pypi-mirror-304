from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ExcludeConstraint
import sqlalchemy.orm as orm

from fr_db.models.base import Base
from fr_db.models.shift_mixin import ShiftMixin


class ActualShift(Base, ShiftMixin):
    __table_args__ = (
        ExcludeConstraint(('employee_id', '='), (sa.text('tsrange(start, "end")'), '&&'), using='gist'),
        {'schema': 'tenant'},
    )

    employee: orm.Mapped['Employee'] = orm.relationship(back_populates="actual_shifts", lazy="noload")

    planned_shift_id: orm.Mapped[UUID | None] = orm.mapped_column(sa.ForeignKey('tenant.planned_shift.id', ondelete="SET NULL"))
    planned_shift: orm.Mapped['PlannedShift'] = orm.relationship(back_populates='actual_shifts', lazy='noload')
