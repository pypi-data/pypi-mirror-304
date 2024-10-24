from enum import Enum

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fr_db.models.base import Base
from fr_db.models.mixins import UUIDTimeStampMixin
# from fr_common_lib.connections.s3.settings import settings as s3_settings


class SizeType(Enum):
    W48H48 = (48, 48)
    W256H256 = (256, 256)
    W1280H720 = (1280, 720)
    ORIGIN = (None, None)


ImageSizeType = Enum("ImageTypeSize", {item.name: item.name for item in SizeType}, type=str)

class Image(Base, UUIDTimeStampMixin):


    __table_args__ = ({'schema': 'tenant'},)

    # path: orm.Mapped[str] = orm.mapped_column(sa.String(60))
    width: orm.Mapped[int] = sa.Numeric(precision=4, scale=0)
    height: orm.Mapped[int] = sa.Numeric(precision=4, scale=0)

    size_type: orm.Mapped[ImageSizeType] = orm.mapped_column(sa.String(10))

    # @property
    # def url(self):
    #     return f'https://{s3_settings.DEFAULT_BUCKET_HOST}/{self.id}'

