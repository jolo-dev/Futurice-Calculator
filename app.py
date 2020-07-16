from flask import Flask, render_template, request
import base64
from routes.calculus import configure_routes


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


configure_routes(app)

if __name__ == "__main__":
    app.run()
