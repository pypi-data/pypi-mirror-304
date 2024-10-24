import sqlalchemy as sa
import sqlalchemy.orm as orm


from fr_db.models.base import Base
from fr_db.models.mixins import UUIDTimeStampMixin


class Company(Base, UUIDTimeStampMixin):

    __table_args__ = ({'schema': 'tenant'},)

    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    departments: orm.Mapped[list["Department"]] = orm.relationship(back_populates="company", lazy="noload")
