import app
import models
from flask_migrate import Migrate

import sqlalchemy
import config


def open_db(db_name, password, owner='postgres', host='localhost', port='5432'):
    engine = sqlalchemy.create_engine(f'postgresql://{owner}:{password}@'
                                      f'{host}:{port}/{db_name}')
    return engine.connect()


def open_or_create_db():
    try:
        connection = open_db(config.postgres_db_name,
                             config.postgres_password,
                             config.postgres_owner,
                             config.postgres_host,
                             config.postgres_port)
    except sqlalchemy.exc.OperationalError:
        connection = open_db('postgres', 'postgres', 'postgres', 'localhost', '5432')
        connection.execute('COMMIT')
        connection.execute(f'CREATE DATABASE {config.postgres_db_name} '
                           f'WITH OWNER = {config.postgres_owner};')
        connection = open_db(config.postgres_db_name,
                             config.postgres_password,
                             config.postgres_owner,
                             config.postgres_host,
                             config.postgres_port)
    return connection


open_or_create_db().close()
application = app.app
migrate = Migrate(application, app.db)
