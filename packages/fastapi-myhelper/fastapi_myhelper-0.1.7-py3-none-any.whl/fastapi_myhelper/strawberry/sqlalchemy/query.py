from strawberry.types import Info
from strawberry.types.info import Selection
from sqlalchemy.sql import Select
from sqlalchemy.orm import Load, joinedload, load_only
from sqlalchemy.future import select
from typing import TypedDict
import re


class ProcessResult(TypedDict):
    fields: list[str]
    relations: list['ProcessResult']


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


# code source https://habr.com/ru/articles/723220/
def flatten(items: list):
    if not items:
        return items
    if isinstance(items[0], list):
        return flatten(items[0]) + flatten(items[1:])
    return items[:1] + flatten(items[1:])


def get_relation_options(relation: dict[str, ProcessResult], prev_sql: Load = None):
    key, val = next(iter(relation.items()))
    fields = val['fields']
    relations = val['relations']
    if prev_sql:
        sql = prev_sql.joinedload(key).load_only(*fields)
    else:
        sql = joinedload(key).load_only(*fields)
    if not relations:
        return sql
    if len(relations) == 1:
        return get_relation_options(relations[0], sql)
    result = []
    for rel in relations:
        rels = get_relation_options(rel, sql)
        if hasattr(rels, '__iter__'):
            for r in rels:
                result.append(r)
        else:
            result.append(rels)
    return result


def query_to_select(
        base_table,
        info: Info,
) -> Select:
    def process_items(
            items: list[Selection],
            table,
    ) -> ProcessResult:
        fields, relations = [], []
        for item in items:
            if item.name == '__typename':
                continue
            try:
                relation = getattr(table, camel_to_snake(item.name))
            except AttributeError:
                continue
            if not len(item.selections):
                fields.append(relation)
                continue
            related_class = relation.property.mapper.class_
            relations.append({relation: process_items(item.selections, related_class)})
        return {'fields': fields, 'relations': relations}

    selections = info.selected_fields[0].selections
    options = process_items(selections, base_table)

    fields = [load_only(*options['fields'])] if len(options['fields']) else []

    query_options = [
        *fields,
        *flatten([get_relation_options(rel) for rel in options['relations']])
    ]

    return select(base_table).options(*query_options)