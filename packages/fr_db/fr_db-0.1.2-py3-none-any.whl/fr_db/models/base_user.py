import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models.base import Base
from fr_db.models.mixins import UUIDTimeStampMixin


class BaseUser(Base, UUIDTimeStampMixin):

    __table_args__ = ({'schema': 'shared'},)

    type: orm.Mapped[str]

    __mapper_args__ = {
        'polymorphic_identity': 'BaseUser',
        'polymorphic_on': 'type'
    }

    customer_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("shared.customer.id", ondelete='CASCADE'))
    customer: orm.Mapped["Customer"] = orm.relationship(back_populates="users", lazy="noload")

    sessions: orm.Mapped[list['AuthSession']] = orm.relationship(back_populates='user', lazy='noload')
