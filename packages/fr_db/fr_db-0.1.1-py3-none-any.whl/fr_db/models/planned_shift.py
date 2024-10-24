import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ExcludeConstraint
import sqlalchemy.orm as orm

from fr_db.models.base import Base
from fr_db.models.shift_mixin import ShiftMixin


class PlannedShift(Base, ShiftMixin):

    __table_args__ = (
        ExcludeConstraint(('employee_id', '='), (sa.text('tsrange(start, "end")'), '&&'), using='gist'),
        {'schema': 'tenant'},
    )

    employee: orm.Mapped["Employee"] = orm.relationship(back_populates="planned_shifts", lazy="noload")
    actual_shifts: orm.Mapped[list['ActualShift']] = orm.relationship(back_populates='planned_shift', lazy='noload')

