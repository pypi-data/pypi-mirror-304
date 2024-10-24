import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models.base import Base
from fr_db.models.mixins import TimestampMixin


class Customer(Base, TimestampMixin):

    __table_args__ = ({'schema': 'shared'},)

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True, autoincrement=True)

    users: orm.Mapped[list["User"]] = orm.relationship(back_populates="customer", lazy="noload")

    @property
    def db_schema(self) -> str:
        return f't{str(self.id)}'
