import sqlalchemy as sa

from fr_db.models.base import Base

link_department_employee = sa.Table(
    "link_department_employee",
    Base.metadata,
    sa.Column("department_id", sa.ForeignKey("tenant.department.id"), primary_key=True),
    sa.Column("employee_id", sa.ForeignKey("tenant.employee.id"), primary_key=True),
    schema="tenant"
)


link_follower_followee = sa.Table(
    "link_follower_followee",
    Base.metadata,
    sa.Column("employee_from_id", sa.ForeignKey("tenant.employee.id"), primary_key=True),
    sa.Column("employee_to_id", sa.ForeignKey("tenant.employee.id"), primary_key=True),
    schema="tenant"
)
