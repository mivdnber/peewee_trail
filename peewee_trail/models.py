import collections
from peewee import *

class DateTimeTZRangeField(Field):
    '''A field that implements the tstzrange PostgreSQL type'''
    db_field = 'tstzrange'

class HistoryBase(Model):
    id = IntegerField()

class History(Model):
    '''A mixin class that tracks changes to your peewee models.'''
    _history = None
    sys_period = DateTimeTZRangeField(constraints=[SQL('default tstzrange(current_timestamp, null)')])

    @classmethod
    def history(cls):
        '''Returns a model that holds historical entries for the model it's
        called on'''

        # Create a model identical to the model inheriting History to hold
        # previous versions of the model
        if cls._history is None:
            def copy_fk(fk):
                ''''creates a new ForeignKeyField based on another one, but with
                a different related_name to prevent conflicts'''
                return ForeignKeyField(fk.rel_model,
                    related_name=fk.related_name + '_history',
                    on_delete='CASCADE',
                    on_update='CASCADE',
                    to_field=fk.to_field
                )

            # Override the foreign keys. Using an OrderedDict to maintain
            # column order.
            attrs = collections.OrderedDict([
                (name, copy_fk(getattr(cls, name)))
                for name in dir(cls)
                if isinstance(getattr(cls, name), ForeignKeyField)
            ])

            class HistoryMeta:
                database = cls._meta.database

            attrs['Meta'] = HistoryMeta

            # Dynamically create the new model
            cls._history = type(cls.__name__ + 'History', (HistoryBase, cls), attrs)
        return cls._history

    @classmethod
    def all_versions(cls, *selection):
        '''Returns a query that selects the current version followed by
        all previous versions.

        :param selection: arguments passed to :meth:`Model.select`
        '''
        return cls.select(*selection).union_all(cls.history().select(*selection))

    @classmethod
    def create_table(cls, fail_silently=False, with_history=True):
        '''Creates the model's table along with its history table. See
        :meth:`Model.create_table` for information about the parameters.
        '''
        ret = super(History, cls).create_table(fail_silently)
        if with_history:
            cls.history().create_table(fail_silently, with_history=False)
            database = cls._meta.database
            database.execute_sql('''
                create trigger versioning_trigger
                before insert or update or delete on %s
                for each row execute procedure versioning(
                    'sys_period', '%s', true
                )
            ''' % (cls._meta.db_table, cls.history()._meta.db_table))

    @classmethod
    def drop_table(cls, fail_silently=False, cascade=False, with_history=True):
        super(History, cls).drop_table(fail_silently=fail_silently, cascade=cascade)
        if with_history:
            cls.history().drop_table(fail_silently=fail_silently, cascade=cascade, with_history=False)

    @classmethod
    def _drop_only_this_table(cls, fail_silently=False, cascade=False):
        super(History, cls).drop_table(fail_silently=fail_silently, cascade=cascade)

    @property
    def versions(self):
        '''Returns a query that selects all previous versions of the model
        instance and any changes made to them from version to version'''

        return self.select(
            self.__class__,
            SQL("hstore(t1.*) - lead(hstore(t1.*)) over(order by t1.sys_period desc) - ARRAY['sys_period']").alias('changes')
        ).from_(
            self.all_versions().alias('t1')
        ).where(
            self.__class__.id == self.id
        )
