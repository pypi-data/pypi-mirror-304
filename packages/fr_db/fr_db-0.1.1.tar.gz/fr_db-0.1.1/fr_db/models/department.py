from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, relationship

from fr_db.models.base import Base
from fr_db.models.links import link_department_employee
from fr_db.models.mixins import UUIDTimeStampMixin


class Department(Base, UUIDTimeStampMixin):

    __table_args__ = ({'schema': 'tenant'},)

    name: Mapped[str] = mapped_column(sa.String(50))
    description: Mapped[str | None] = mapped_column(sa.String(200))

    company_id: Mapped[UUID | None] = mapped_column(sa.ForeignKey('tenant.company.id'))
    company: Mapped["Company"] = relationship(back_populates="departments", lazy="noload")

    parent_id: Mapped[UUID | None] = mapped_column(sa.ForeignKey("tenant.department.id"))
    parent: Mapped["Department"] = relationship("Department", back_populates="children",
                                                              remote_side="Department.id")

    children: Mapped[list["Department"]] = relationship("Department", back_populates="parent",
                                                                      lazy="noload")

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="departments", secondary=link_department_employee, lazy="noload")

    gates: Mapped[list["Gate"]] = relationship(back_populates="department", lazy="noload")