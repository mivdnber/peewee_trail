.. getting-started Getting started

Getting started
===============

Requirements
------------

``peewee_trail`` uses the temporal_tables_ PostgreSQL extension. As such,
only PostgreSQL 9.2+ is supported.

The easiest way to install ``temporal_tables`` is using the pgxn_ client::

    $ pgxn install temporal_tables

See the `pgxn client docs <pgxn_>`_ for more information.

Before using ``peewee_trail``, make sure to register the extension in your database::

    create extension temporal_tables


Installation
------------

I recommend installing ``peewee_trail`` with ``pip``::

    $ pip install peewee_trail

If you want to install it manually, I assume you're smart enough to figure it
out.

Your first temporal model
-------------------------

LOL!

.. _temporal_tables: http://pgxn.org/dist/temporal_tables/
.. _pgxn: http://pgxnclient.projects.pgfoundry.org/
