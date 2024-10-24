from enum import Enum
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import relationship

from fr_db.models import Base
from fr_db.models.mixins import UUIDTimeStampMixin


class SessionStatus(Enum):
    ACTIVE = 'active'
    COMPLETED = "completed"
    EXPIRED = "expired"
    REVOKED = "revoked"
    HACKED = "hacked"


class AuthSession(Base, UUIDTimeStampMixin):

    __table_args__ = (
        {'schema': 'shared'},
    )


    tokens: orm.Mapped[list['RefreshToken']] = orm.relationship(back_populates='session', passive_deletes=True)

    user_id: orm.Mapped[UUID] = orm.mapped_column(sa.ForeignKey('shared.base_user.id', ondelete='CASCADE'))
    user: orm.Mapped['User'] = orm.relationship(back_populates='sessions', lazy='noload')

    ip_addr: orm.Mapped[str] = orm.mapped_column(sa.String(45))

    status: orm.Mapped[SessionStatus] = orm.mapped_column(sa.Enum(SessionStatus, native_enum=False), default=SessionStatus.ACTIVE, nullable=False)

    active_token: orm.Mapped['RefreshToken'] = relationship(
        'RefreshToken',
        primaryjoin=f"and_(RefreshToken.session_id == AuthSession.id, RefreshToken.expires_at > func.now(), AuthSession.status == 'ACTIVE')",
        order_by="desc(RefreshToken.expires_at)",
        uselist=False,
        viewonly=True,
    )
