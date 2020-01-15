from flask_script import Manager
from app import createApp
from flask_migrate import MigrateCommand

app = createApp()

manager = Manager(app)

manager.add_command('db', MigrateCommand)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
