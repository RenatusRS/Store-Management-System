from os import path
from shutil import rmtree

from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database, drop_database

from config_authentication import Configuration
from models import database, User

dirpath = "/opt/src/authentication/migrations"

if path.exists(dirpath) and path.isdir(dirpath):
    rmtree(dirpath)

application = Flask(__name__)
application.config.from_object(Configuration)

migrateObject = Migrate(application, database)

while True:
    try:
        if database_exists(application.config["SQLALCHEMY_DATABASE_URI"]):
            drop_database(application.config["SQLALCHEMY_DATABASE_URI"])

        create_database(application.config["SQLALCHEMY_DATABASE_URI"])

        database.init_app(application)

        with application.app_context() as context:
            init()
            migrate(message="Authentication migration")
            upgrade()

            database.session.add(User(
                forename="admin",
                surname="admin",
                email="admin@admin.com",
                password="1",
                role="admin"
            ))
            database.session.commit()

            while True:
                pass

    except Exception as error:
        print(error, flush=True)
