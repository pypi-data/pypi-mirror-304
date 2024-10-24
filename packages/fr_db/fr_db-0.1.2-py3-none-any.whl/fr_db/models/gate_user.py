import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models import BaseUser


class GateUser(BaseUser):

    __table_args__ = ({'schema': 'shared'},)

    __mapper_args__ = {
        'polymorphic_identity': 'GateUser'
    }

    id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("shared.base_user.id", ondelete='CASCADE'), primary_key=True)

    username: orm.Mapped[str] = orm.mapped_column(sa.String(50), unique=True)
    password: orm.Mapped[str] = orm.mapped_column(sa.String(256))

    gate: orm.Mapped['Gate'] = orm.relationship(back_populates='user', lazy='noload')