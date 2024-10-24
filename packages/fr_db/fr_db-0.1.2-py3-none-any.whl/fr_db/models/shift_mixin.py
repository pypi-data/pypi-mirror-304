import datetime as dt
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models.mixins import TimezoneMixin, UUIDTimeStampMixin


class ShiftMixin(TimezoneMixin, UUIDTimeStampMixin):

    start: orm.Mapped[dt.datetime | None] = orm.mapped_column(sa.TIMESTAMP, nullable=True)
    end: orm.Mapped[dt.datetime | None] = orm.mapped_column(sa.TIMESTAMP, nullable=True)
    employee_id: orm.Mapped[UUID | None] = orm.mapped_column(sa.ForeignKey("tenant.employee.id", ondelete='CASCADE'))

