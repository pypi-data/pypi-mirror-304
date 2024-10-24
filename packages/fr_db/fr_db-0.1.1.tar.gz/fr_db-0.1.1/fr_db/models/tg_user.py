import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models import BaseUser


class TgUser(BaseUser):

    __table_args__ = ({'schema': 'shared'},)

    __mapper_args__ = {
        'polymorphic_identity': 'TgUser'
    }

    id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("shared.base_user.id", ondelete='CASCADE'), primary_key=True)