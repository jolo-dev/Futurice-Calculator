from flask import Flask, render_template, request
import base64
import operator
import re


app = Flask(__name__)


ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/calculus")
def calculus():
    query = check_padding(request.args.get("query"))
    result = eval(query)
    status = 200
    if not result:
        result = "Error: " + str(result)
        status = 406
        print(result.isnumeric())
    return {"result": result, "status": status}


def check_padding(b64_string):
    if len(b64_string) % 4 != 0:  # check if multiple of 4
        while len(b64_string) % 4 != 0:
            b64_string = b64_string + "="
        req_str = base64.b64decode(b64_string)
    else:
        req_str = base64.b64decode(b64_string)
    return req_str.decode("utf-8")


if __name__ == "__main__":
    app.run()
