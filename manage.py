from app import createApp
from app.api.error.errorHandler import Success

app = createApp()


@app.route('/')
def hello_world():
    return Success(information="your project is running now~ (◕ᴗ◕✿)")


if __name__ == '__main__':
    app.run()
