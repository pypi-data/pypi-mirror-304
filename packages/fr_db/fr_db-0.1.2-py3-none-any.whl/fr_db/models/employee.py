from datetime import date
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models import link_department_employee
from fr_db.models.base import Base
from fr_db.models.mixins import UUIDTimeStampMixin


class Employee(Base, UUIDTimeStampMixin):

    __table_args__ = ({'schema': 'tenant'},)

    first_name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    middle_name: orm.Mapped[str | None] = orm.mapped_column(sa.String(50))
    last_name: orm.Mapped[str] = orm.mapped_column(sa.String(50))

    birthdate: orm.Mapped[date | None] = orm.mapped_column(sa.Date)

    position: orm.Mapped[str | None] = orm.mapped_column(sa.String(50))
    code: orm.Mapped[str | None] = orm.mapped_column(sa.String(11), unique=True)

    departments: orm.Mapped[list["Department"]] = orm.relationship(
        back_populates="employees", secondary=link_department_employee, lazy="noload")

    photos: orm.Mapped[list["Photo"]] = orm.relationship(back_populates="employee", lazy="noload")

    avatar: orm.Mapped["Photo"] = orm.relationship(
        back_populates="employee",
        primaryjoin="and_(Employee.id==Photo.employee_id, Photo.avatar==True)",
        uselist=False, viewonly=True, lazy="noload")

    followers: orm.Mapped[list["Employee"]] = orm.relationship(
        back_populates="followees",
        secondary='tenant.link_follower_followee',
        primaryjoin="Employee.id == tenant.link_follower_followee.c.employee_to_id",
        secondaryjoin="Employee.id == tenant.link_follower_followee.c.employee_from_id",
        lazy="noload")

    followees: orm.Mapped[list["Employee"]] = orm.relationship(
        back_populates="followers",
        secondary='tenant.link_follower_followee',
        primaryjoin="Employee.id == tenant.link_follower_followee.c.employee_from_id",
        secondaryjoin="Employee.id == tenant.link_follower_followee.c.employee_to_id",
        lazy="noload")

    recogn_assocs: orm.Mapped[list["RecognAssoc"]] = orm.relationship(back_populates='employee', lazy="noload")

    actual_shifts: orm.Mapped[list["ActualShift"]] = orm.relationship(back_populates="employee", lazy="noload")
    planned_shifts: orm.Mapped[list["PlannedShift"]] = orm.relationship(back_populates='employee', lazy="noload")

    unplanned_shifts: orm.Mapped[list["ActualShift"]] = orm.relationship(
        back_populates="employee", viewonly=True, lazy="noload",
        primaryjoin="and_(Employee.id==ActualShift.employee_id, ActualShift.planned_shift_id==None)"
    )

    opened_shift: orm.Mapped["ActualShift"] = orm.relationship(back_populates="employee", lazy="noload",
        primaryjoin='and_(Employee.id==ActualShift.employee_id, ActualShift.end==None)',
        uselist=False, viewonly=True)

    user: orm.Mapped["User"] = orm.relationship(back_populates='employee', lazy="noload")
    user_id: orm.Mapped[UUID | None] = orm.mapped_column(sa.ForeignKey('shared.user.id'), unique=True)
