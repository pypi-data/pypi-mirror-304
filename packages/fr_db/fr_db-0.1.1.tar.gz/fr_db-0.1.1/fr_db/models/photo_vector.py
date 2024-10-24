from uuid import UUID

# import numpy as np
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.ext.hybrid import hybrid_property

from fr_db.models import Base
from fr_db.models.mixins import TimestampMixin


class PhotoVector(Base, TimestampMixin):

    __table_args__ = ({'schema': 'tenant'},)

    value: orm.Mapped[list[float]] = orm.mapped_column(pg.ARRAY(sa.Float, dimensions=1))

    vectorizeable_id: orm.Mapped[UUID] = orm.mapped_column(
        sa.ForeignKey("tenant.vectorizeable.id", ondelete='CASCADE'), primary_key=True)
    vectorizeable: orm.Mapped['Vectorizeable'] = orm.relationship(back_populates='vector', uselist=False)

    # @hybrid_property
    # def np_array(self):
    #     return np.array(self.value)
