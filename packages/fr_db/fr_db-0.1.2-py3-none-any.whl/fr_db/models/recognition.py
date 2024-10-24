import uuid

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models.mixins import TimezoneMixin
from fr_db.models.vectorizeable import Vectorizeable
# from app.schemas.recognition_errors import RecognitionErrors as RecognizeErrors

# RecognitionErrors = enum.Enum("RecognitionErrors", {item: item for item in RecognizeErrors.get_registered()}, type=str)


class Recognition(Vectorizeable, TimezoneMixin):

    __table_args__ = ({'schema': 'tenant'},)

    __mapper_args__ = {
        'polymorphic_identity': 'Recognition'
    }

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.ForeignKey("tenant.vectorizeable.id"), primary_key=True,
    )

    gate_id: orm.Mapped[uuid.UUID] = orm.mapped_column(sa.ForeignKey("tenant.gate.id",ondelete='CASCADE'))
    gate: orm.Mapped["Gate"] = orm.relationship(back_populates="recognitions", lazy="noload")

    error: orm.Mapped[str|None] = orm.mapped_column(sa.String(40))