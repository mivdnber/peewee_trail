from pytest import *
from playhouse.postgres_ext import PostgresqlExtDatabase, register_hstore
from peewee import Model, TextField, IntegerField, ForeignKeyField
from pytest_dbfixtures.plugin import postgresql
import psycopg2
from psycopg2 import extensions as pg_extensions

class PostgresqlExtDatabaseFromConnection(PostgresqlExtDatabase):
    '''This is a dirty hack to pass an already instanciated psycopg2 connction
    to PostgresqlExtDatabase. Don't get any ideas.
    '''

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
        cur.execute('''
            create extension hstore;
            create extension temporal_tables;
        ''')

    db = PostgresqlExtDatabaseFromConnection(postgresql, register_hstore=False)
    db.connect()
    yield db
    db.close()

@yield_fixture
def models(db):
    from peewee_trail import History

    class BaseModel(Model):
        class Meta(object):
            database = db

    class BasicModel(BaseModel, History):
        foo = TextField()
        bar = IntegerField()


    class ReferencedModel(BaseModel):
        lol = TextField()

    class FKModel(BaseModel, History):
        ref = ForeignKeyField(ReferencedModel, on_delete='CASCADE', related_name='haha')

    class models:
        pass

    all_models = [BasicModel, ReferencedModel, FKModel]

    for m in all_models:
        setattr(models, m.__name__, m)

    #import pdb; pdb.set_trace()
    db.create_tables(all_models)
    yield models
    db.drop_tables(all_models)
