import datetime as dt
import uuid

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models.base import Base


class RecognAssoc(Base):

    __table_args__ = ({'schema': 'tenant'},)

    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sa.func.now())

    left_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.ForeignKey('tenant.vectorizeable.id',ondelete='CASCADE'), primary_key=True)
    left: orm.Mapped["Vectorizeable"] = orm.relationship(
        back_populates="child_assocs", lazy="noload", foreign_keys=left_id)

    right_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.ForeignKey('tenant.vectorizeable.id', ondelete='CASCADE'), primary_key=True)
    right: orm.Mapped['Vectorizeable'] = orm.relationship(back_populates='parent_assocs',
                                                  lazy='noload', foreign_keys=right_id)

    employee_id: orm.Mapped[uuid.UUID] = orm.mapped_column(sa.ForeignKey('tenant.employee.id',ondelete='CASCADE'))
    employee: orm.Mapped['Employee'] = orm.relationship(back_populates='recogn_assocs', lazy='noload')

    diff: orm.Mapped[float]
    accepted: orm.Mapped[bool | None] = orm.mapped_column(sa.Boolean, nullable=True, default=None)

    base: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.text('FALSE'))

    # @hybrid_property
    # def outlier(self) -> bool:
    #     return self.diff > settings.FACE_RECOGNITION_LIMIT
    #
    # @outlier.expression
    # def outlier(cls) -> bool:
    #     return sa.text("diff > :limit").params(limit=settings.FACE_RECOGNITION_LIMIT)

    recogn_assoc_base_employee_id_created_at = sa.Index(
        'recogn_assoc_base_employee_id_created_at',
        employee_id, created_at.desc(), unique=True, postgresql_where="base = True")