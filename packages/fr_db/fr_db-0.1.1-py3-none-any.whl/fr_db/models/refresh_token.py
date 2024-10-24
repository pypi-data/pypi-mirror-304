from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import ForeignKey
import sqlalchemy.orm as orm

from fr_db.models import Base
from fr_db.models.mixins import UUIDTimeStampMixin


class RefreshToken(Base, UUIDTimeStampMixin):

    __table_args__ = ({'schema': 'shared'},)

    session_id: orm.Mapped[UUID] = orm.mapped_column(ForeignKey('shared.auth_session.id', ondelete='CASCADE'))
    session: orm.Mapped['AuthSession'] = orm.relationship(back_populates='tokens', lazy='noload')

    parent_id: orm.Mapped[UUID] = orm.mapped_column(
        ForeignKey('shared.refresh_token.id', ondelete='SET NULL'),nullable=True)
    parent: orm.Mapped['RefreshToken'] = orm.relationship('RefreshToken', remote_side='RefreshToken.id', lazy='noload')

    expires_at: orm.Mapped[datetime] = orm.mapped_column(sa.TIMESTAMP(timezone=True), nullable=False)
