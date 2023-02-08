from __future__ import annotations

import glob
import subprocess
import sys
import tempfile
from typing import Optional, Type, Any, Literal
from types import TracebackType

import psycopg
from psycopg.connection import Connection


class RunPostgres:
    def __init__(self, database: Optional[str] = None):
        pgbins = glob.glob("/usr/lib/postgresql/*/bin")
        if len(pgbins) == 0:
            raise RuntimeError("Cannot find postgres commands")
        self.pgbin = pgbins[0]
        self.database = database

    def __enter__(self) -> RunPostgres:
        self.tmp = tempfile.TemporaryDirectory()
        tmp = self.tmp.__enter__()
        try:
            subprocess.check_call(
                [f"{self.pgbin}/pg_ctl", "init", "-D", tmp, "-l", f"{tmp}/log"]
            )
            subprocess.check_call(
                [
                    f"{self.pgbin}/pg_ctl",
                    "start",
                    "-D",
                    tmp,
                    "-l",
                    f"{tmp}/log",
                    "-w",
                    "-o",
                    f'-h "" -k {tmp}',
                ]
            )
            self.host: Optional[str] = f"{tmp}"
            if self.database:
                with psycopg.connect(
                    f"postgresql:///postgres?host={tmp}", autocommit=True
                ) as db:
                    with db.cursor() as cur:
                        cur.execute(f"CREATE DATABASE {self.database}")
        except Exception:
            self.__exit__(*sys.exc_info())
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> Literal[False]:
        self.host = None
        subprocess.call(
            [f"{self.pgbin}/pg_ctl", "stop", "-D", self.tmp.name, "-w", "-m", "i"]
        )
        self.tmp.__exit__(exc_type, exc, traceback)
        return False

    def connect(self, **kwargs) -> Any:
        return psycopg.connect(
            dbname=self.database or "postgres", host=self.host, **kwargs
        )


class ClassPostgres:
    def __init__(self, postgresql: Connection[Any]):
        self.postgresql = postgresql
        self.classes: dict[str, type] = {}

    def cursor(self, *args, **kwargs) -> Any:
        return self.postgresql.cursor(*args, **kwargs)

    def class_cursor(self, class_name: str, *args, **kwargs) -> Any:
        cls = self.classes.get(class_name)
        if not cls:
            raise ValueError(f"No such class: {class_name}")
        return self.postgresql.cursor(
            *args, row_factory=psycopg.rows.class_row(cls), **kwargs
        )
