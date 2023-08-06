from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, UniqueConstraint, PrimaryKeyConstraint
from functools import reduce


def attrs_name_equality(first_attr, second_attr) -> bool:
    first_attr_name = (
        first_attr.property.key
        if isinstance(first_attr, InstrumentedAttribute)
        else first_attr.key
    )
    second_attr_name = (
        second_attr.property.key
        if isinstance(second_attr, InstrumentedAttribute)
        else second_attr.key
    )
    return first_attr_name == second_attr_name


def get_unique_columns(table) -> list[str]:
    return [
        column.name
        for column in table.columns
        if any([column.primary_key, column.unique])
    ]


def get_unique_constraint_columns(table) -> list[tuple[str, ...]]:
    return [
        tuple(column.name for column in constraint.columns)
        for constraint in table.constraints
        if isinstance(constraint, (UniqueConstraint, PrimaryKeyConstraint)) and len(constraint.columns) > 1
    ]


async def get_non_unique_fields(
        model,
        data,
        session: AsyncSession,
) -> list[str]:
    fields = get_unique_columns(model.__table__)
    constraint_fields = get_unique_constraint_columns(model.__table__)
    selects = []
    for field in fields:
        model_field = getattr(model, field)
        value = getattr(data, field, None)
        qs = None
        if value is not None:
            qs = select(model_field).where(model_field == value).limit(1).scalar_subquery().exists()
        selects.append(qs)
    for constraint in constraint_fields:
        values = {
            getattr(model, field): getattr(data, field, None)
            for field in constraint
        }
        where = reduce(
            lambda prev, column: (column == values[column]) & (prev if prev is not None else True),
            values, None
        )
        selects.append(
            select(*values.keys()).where(where).scalar_subquery().exists()
        )

    result = (await session.execute(select(*selects))).one_or_none()
    non_unique = []
    for i, field in enumerate(fields + constraint_fields):
        if result[i]:
            non_unique.append(field)
    return non_unique
