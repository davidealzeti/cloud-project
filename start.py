from flask import Flask
import os
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    port = os.getenv("WEBPORT", 6000)
    host = os.getenv("WEBHOST", "0.0.0.0")
    app.run(host=host, port=port)

