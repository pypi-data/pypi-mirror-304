from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models import BaseUser


class User(BaseUser):

    __table_args__ = ({'schema': 'shared'},)

    __mapper_args__ = {
        'polymorphic_identity': 'User'
    }

    id: orm.Mapped[UUID] = orm.mapped_column(sa.ForeignKey("shared.base_user.id", ondelete='CASCADE'), primary_key=True)
    is_super: orm.Mapped[bool | None]
    email: orm.Mapped[str] = orm.mapped_column(sa.String(50), unique=True)
    phone: orm.Mapped[str | None] = orm.mapped_column(sa.String(11), unique=True)

    employee: orm.Mapped['Employee'] = orm.relationship(back_populates='user', lazy='noload')

