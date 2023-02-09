from dataclasses import dataclass

from pypog import RunPostgres, ClassPostgres

import psycopg


@dataclass
class Test:
    id: int
    num: int
    data: str


def test_run_postgres():
    with RunPostgres("test") as pg:
        with pg.connect() as db:
            db.execute(
                "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);"
            )
            db.execute("INSERT INTO test (num, data) VALUES (%s, %s);", [42, "42"])

        with pg.connect() as db:
            cpg = ClassPostgres(db)
            # cpg.classes["test"] = Test

            with cpg.class_cursor("test") as cur:
                cur.execute("SELECT * FROM test")
                for t in cur:
                    print("!!!", t)
