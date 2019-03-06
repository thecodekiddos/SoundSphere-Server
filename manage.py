from flask_script import Manager, prompt_bool

from soundsphere import create_app
from soundsphere.database import db

manager = Manager(create_app)


@manager.command
def dbcreate():
    "Creates database tables from SQLAlchemy models"
    db._create_database()


@manager.command
def dbdrop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        db._drop_database()


if __name__ == "__main__":
    manager.run()
