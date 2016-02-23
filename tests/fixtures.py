from pytest import *
from peewee import *
from playhouse.postgres_ext import *
from pytest_dbfixtures.plugin import postgresql
import psycopg2
from psycopg2 import extensions as pg_extensions

class PostgresqlExtDatabaseFromConnection(PostgresqlExtDatabase):
    def _connect(self, database, encoding=None, **kwargs):
        if not psycopg2:
            raise ImproperlyConfigured('psycopg2 must be installed.')
        conn = database
        if self.register_unicode:
            pg_extensions.register_type(pg_extensions.UNICODE, conn)
            pg_extensions.register_type(pg_extensions.UNICODEARRAY, conn)
        if encoding:
            conn.set_client_encoding(encoding)

        if self.register_hstore:
            register_hstore(conn, globally=True)

        return conn

@yield_fixture
def db(postgresql):
    with postgresql.cursor() as cur:
        cur.execute('create extension hstore')

    db = PostgresqlExtDatabaseFromConnection(postgresql)
    db.connect()
    yield db
    db.close()

@yield_fixture
def models(db):
    class models:
        class BaseModel(Model):
            class Meta(object):
                database = db

        class BasicModel(BaseModel):
            foo = TextField()
            bar = IntegerField()

    db.create_tables([models.BasicModel])
    yield models
    db.drop_tables([models.BasicModel])
