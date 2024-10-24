
from fr_db.models import Base
import sqlalchemy.orm as orm
from fr_db.models.mixins import UUIDTimeStampMixin, HasThumbnails


class Vectorizeable(Base, UUIDTimeStampMixin, HasThumbnails):
    __table_args__ = ({'schema': 'tenant'},)

    type: orm.Mapped[str]
    lv_score: orm.Mapped[float | None]

    vector: orm.Mapped['PhotoVector'] = orm.relationship(back_populates='vectorizeable', lazy='noload')

    __mapper_args__ = {
        'polymorphic_identity': 'Vectorizeable',
        'polymorphic_on': 'type'
    }

    parent_assocs: orm.Mapped[list["RecognAssoc"]] = orm.relationship(
        back_populates='right', cascade="all, delete-orphan", lazy="noload",
        foreign_keys="RecognAssoc.right_id")

    child_assocs: orm.Mapped[list["RecognAssoc"]] = orm.relationship(
        back_populates='left', cascade="all, delete-orphan", lazy="noload",
        foreign_keys="RecognAssoc.left_id")
