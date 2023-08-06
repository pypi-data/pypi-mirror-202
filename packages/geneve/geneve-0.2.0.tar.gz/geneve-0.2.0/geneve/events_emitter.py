# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Functions for generating event documents that would trigger a given rule."""

from collections import namedtuple
from datetime import datetime, timedelta, timezone
from itertools import chain

from .events_emitter_eql import collect_constraints as collect_constraints_eql
from .events_emitter_eql import get_ast_stats  # noqa: F401
from .solver import emit_field
from .utils import deep_merge, random

__all__ = ("SourceEvents",)

default_custom_schema = {
    "file.Ext.windows.zone_identifier": {
        "type": "long",
    },
    "process.parent.Ext.real.pid": {
        "type": "long",
    },
}

QueryGuess = namedtuple("QueryGuess", ["query", "type", "language", "ast"])
Event = namedtuple("Event", ["meta", "doc"])


def ast_from_eql_query(query):
    import eql

    with eql.parser.elasticsearch_syntax, eql.parser.ignore_missing_functions:
        return eql.parse_query(query)


def ast_from_kql_query(query):
    from . import kql

    return kql.to_eql(query)  # shortcut?


def guess_from_query(query):
    exceptions = []
    try:
        return QueryGuess(query, "eql", "eql", ast_from_eql_query(query))
    except Exception as e:
        exceptions.append(("EQL", e))
    try:
        return QueryGuess(query, "query", "kuery", ast_from_kql_query(query))
    except Exception as e:
        exceptions.append(("Kuery", e))

    def rank(e):
        line = getattr(e[1], "line", -1)
        column = getattr(e[1], "column", -1)
        return (line, column)

    lang, error = sorted(exceptions, key=rank)[-1]
    raise ValueError(f"{lang} query error: {error}")


def ast_from_rule(rule):
    if rule.type not in ("query", "eql"):
        raise NotImplementedError(f"Unsupported rule type: {rule.type}")
    elif rule.language == "eql":
        return ast_from_eql_query(rule.query)
    elif rule.language == "kuery":
        return ast_from_kql_query(rule.query)
    else:
        raise NotImplementedError(f"Unsupported query language: {rule.language}")


def emit_mappings(fields, schema):
    mappings = {}
    for field in fields:
        try:
            field_type = schema[field]["type"]
        except KeyError:
            field_type = "keyword"
        value = {"type": field_type}
        for part in reversed(field.split(".")):
            value = {"properties": {part: value}}
        deep_merge(mappings, value)
    return mappings


def events_from_branch(branch, schema, timestamp, meta):
    events = []
    for doc in branch.solve(schema):
        if timestamp:
            emit_field(doc, "@timestamp", timestamp[0].isoformat(timespec="milliseconds"))
            timestamp[0] += timedelta(milliseconds=1)
        events.append(Event(meta, doc))
    return events


def events_from_root(root, schema, timestamp):
    return [events_from_branch(branch, schema, timestamp, root.meta) for branch in root]


class SourceEvents:
    schema = {}

    def __init__(self, schema=None):
        self.__roots = []

        if schema is not None:
            self.schema = schema

    @classmethod
    def from_ast(cls, ast, *, meta=None):
        se = SourceEvents()
        se.add_ast(ast, meta=meta)
        return se

    @classmethod
    def from_query(cls, query, *, meta=None):
        se = SourceEvents()
        se.add_query(query, meta=meta)
        return se

    @classmethod
    def from_rule(cls, rule, *, meta=None):
        se = SourceEvents()
        se.add_rule(rule, meta=meta)
        return se

    def add_ast(self, ast, *, meta=None):
        root = collect_constraints_eql(ast)
        root.meta = meta
        self.try_emit(root)
        self.__roots.append(root)
        return root

    def add_query(self, query, *, meta=None):
        ast = guess_from_query(query).ast
        return self.add_ast(ast, meta=meta)

    def add_rule(self, rule, *, meta=None):
        ast = ast_from_rule(rule)
        return self.add_ast(ast, meta=meta)

    def fields(self):
        return set(chain(*(root.fields() for root in self.__roots)))

    def mappings(self, root=None):
        fields = self.fields() if root is None else root.fields()
        return emit_mappings(fields, self.schema)

    def roots(self):
        return iter(self.__roots)

    def emit(self, root=None, *, timestamp=True, complete=False, count=1):
        if timestamp:
            timestamp = [datetime.now(timezone.utc).astimezone()]
        if complete:
            if root:
                events = (events_from_root(root, self.schema, timestamp) for _ in range(count))
            else:
                events = (events_from_root(root, self.schema, timestamp) for _ in range(count) for root in self.__roots)
        else:
            if root:
                events = (events_from_branch(random.choice(root), self.schema, timestamp, root.meta) for _ in range(count))
            else:
                events = (
                    events_from_branch(random.choice(root), self.schema, timestamp, root.meta)
                    for root in random.choices(self.__roots, k=count)
                )
        return list(chain(*events))

    def try_emit(self, root):
        state = random.getstate()
        try:
            _ = events_from_root(root, self.schema, timestamp=False)
        finally:
            random.setstate(state)

    def __iter__(self):
        return self

    def __next__(self):
        return self.emit()

    def __len__(self):
        return len(self.__roots)
