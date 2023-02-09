from dataclasses import dataclass

import psycopg
from pypog import ClassPostgres
from pytest_postgresql import factories


def setup_database(**kwargs):
    with psycopg.connect(**kwargs) as db:
        with db.cursor() as cur:
            cur.execute(
                """CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);
INSERT INTO test (num, data) VALUES (42, '42');
"""
            )


postgresql_proc = factories.postgresql_proc(
    port=None, unixsocketdir="/tmp", load=[setup_database]
)
postgresql = factories.postgresql("postgresql_proc")


def test_pypog(postgresql):
    @dataclass
    class Test:
        id: int
        num: int
        data: str

    cpg = ClassPostgres(postgresql)
    cpg.classes["test"] = Test

    with cpg.class_cursor("test") as cur:
        cur.execute("SELECT * FROM test")
        for t in cur:
            assert isinstance(t, Test)
