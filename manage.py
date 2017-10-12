from cenotes import create_app
from flask_migrate import MigrateCommand, Manager

manager = Manager(create_app)
manager.add_option("-c", "--config", dest="app_settings", required=False)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
