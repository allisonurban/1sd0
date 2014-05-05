from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=80)),
    Column('email', String(length=120)),
    Column('about', String(length=140)),
    Column('last_login', DateTime),
)

sentence = Table('sentence', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', Text),
    Column('puplished_date', DateTime),
    Column('user_id', Integer),
)

sentence = Table('sentence', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', Text),
    Column('published_date', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['about'].create()
    post_meta.tables['user'].columns['last_login'].create()
    pre_meta.tables['sentence'].columns['puplished_date'].drop()
    post_meta.tables['sentence'].columns['published_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['about'].drop()
    post_meta.tables['user'].columns['last_login'].drop()
    pre_meta.tables['sentence'].columns['puplished_date'].create()
    post_meta.tables['sentence'].columns['published_date'].drop()
