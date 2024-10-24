import re
import pydantic as pd
import sqlalchemy as sa
import sqlalchemy.orm as orm
import typing as tp
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declared_attr


class Base(orm.DeclarativeBase):

    __mapper_args__ = {"eager_defaults": True}

    @declared_attr
    def __tablename__(cls):

        def camel_to_snake(name):
            return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return camel_to_snake(cls.__name__)

    @classmethod
    def to_schema(cls, exclude: tp.Iterable[str] | None = None, exclude_uid: bool = True):

        from app.schemas.base import BaseSchema

        exclude = exclude or []
        default_exclude = ['created_at', 'updated_at']
        exclude = exclude + default_exclude

        mapper = inspect(cls)
        fields = {}

        attrs = filter(lambda attr: isinstance(attr, orm.ColumnProperty)
            and attr.columns and not attr.key in exclude, mapper.attrs)

        for attr in attrs:

            column = attr.columns[0]
            if exclude_uid and (str(column.type) == 'NULL' or isinstance(column.type, sa.Uuid)):
                continue

            py_type: type | None = None
            if hasattr(column.type, "impl"):
                if hasattr(column.type.impl, "python_type"):
                    py_type = column.type.impl.python_type
            elif hasattr(column.type, "python_type"):
                py_type = column.type.python_type
            assert py_type, f"Could not infer python_type for {column}"

            field_args = {}

            if isinstance(column.type, sa.String) and column.type.length:
                field_args['max_length'] = column.type.length

            if isinstance(column.type, (sa.Numeric, sa.Float)):
                if column.type.scale:
                    field_args['decimal_places'] = column.type.scale
                if column.type.precision:
                    field_args['max_digits'] = column.type.precision

            default = None
            if column.default is None and not column.nullable:
                default = ...

            fields[attr.key] = (py_type, pd.Field(default, **field_args))

        pd_model = pd.create_model(cls.__name__, **fields, __base__=BaseSchema)
        pd_model._model = cls

        return pd_model
