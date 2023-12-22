import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'database.sqlite',  # current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('migrate-to-v1')
@with_appcontext
def migrate_to_v1():
    # version 1.0.0 introduces sorting feature for nodes,
    # which depends on additional field `sort_order`
    # in `node` table.
    db = get_db()

    cursor = db.cursor()
    cursor.execute('PRAGMA table_info(node);')
    columns_info = cursor.fetchall()
    columns_names = [c['name'] for c in columns_info]

    if 'sort_order' not in columns_names:
        click.echo('Adding missing field `sort_order` to table `node`.')
        cursor.execute('ALTER TABLE `node` ADD `sort_order` INTEGER;')
        cursor.execute('CREATE UNIQUE INDEX `idx_unique_sort_order` ON `node` (`sort_order`);')

        click.echo('Initializing new field `sort_order` with node ID.')
        query = 'UPDATE node SET "sort_order" = id;'
        cursor.execute(query)
        db.commit()

    cursor.close()

    # we have to stop timer manually here
    # otherwise process will run forever
    current_app.eventTable.stopTimer()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    # we have to stop timer manually here
    # otherwise process will run forever
    current_app.eventTable.stopTimer()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(migrate_to_v1)
