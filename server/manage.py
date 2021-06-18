import os
from dotenv import load_dotenv
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

load_dotenv()

from filex import create_app, db, models

app = create_app(mode=os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
