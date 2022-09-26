from flask import Flask
app = Flask(__name__)

import os

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'


if __name__ == "__main__":
    host = os.environ.get('HOST', "0.0.0.0")
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, host=host, port=port)