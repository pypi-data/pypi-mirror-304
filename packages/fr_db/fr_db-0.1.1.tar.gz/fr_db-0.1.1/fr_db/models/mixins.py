import datetime as dt
import uuid

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.dialects.postgresql import UUID as PgUUID

class UUIDMixin:

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()")
    )

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __le__(self, other):
        return self.id <= other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)


class HasThumbnails:
    @orm.declared_attr
    def thumbnails(cls):
        association = sa.Table(
            "link_%s_image" % cls.__tablename__,
            cls.metadata,
            sa.Column("image_id", sa.ForeignKey("tenant.image.id"), primary_key=True),
            sa.Column(
                "%s_id" % cls.__tablename__,
                sa.ForeignKey("tenant.%s.id" % cls.__tablename__),
                primary_key=True,
            ),
            schema='tenant'
        )
        return orm.relationship("Image", secondary=association, lazy='noload')


class TimezoneMixin:

    def header_tz(self):
        from app.core.context import ContextManager

        request = ContextManager.get_context().request
        return int(request.headers.get('tz-offset', 0)) or None

    tz_offset: orm.Mapped[int | None] = orm.mapped_column(
        sa.Numeric(precision=3, scale=0),
        default=header_tz)


class TimestampMixin:
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sa.func.now())
    updated_at: orm.Mapped[dt.datetime] = orm.mapped_column(onupdate=sa.func.now(), server_default=sa.func.now())


class UUIDTimeStampMixin(UUIDMixin, TimestampMixin):
    pass
