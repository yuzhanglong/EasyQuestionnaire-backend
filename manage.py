from app import createApp
from app.utils.templateMaker.templateMaker import pushWJWDataToDB

app = createApp()


@app.route('/')
def hello_world():
    pushWJWDataToDB()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()