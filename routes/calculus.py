from flask import Flask, request
import base64
import json


def configure_routes(app):
    @app.route("/calculus", methods=["GET", "POST"])
    @app.route("/dev/calculus", methods=["GET", "POST"])
    def calculus():
        if request.method == "POST":
            query = convert_to_base64(request.form["calculus-string"])
        elif request.method == "GET":
            query = request.args.get("query")
        if len(query) >= 4:
            checked_query = check_padding(query)
            try:
                result = eval(checked_query)
                if isfloat(result):
                    status = 200
                    error = False
                else:
                    result = "Error with your input: " + query
                    error = True
                    status = 406
            except:
                result = "Error with your input: " + str(query)
                error = True
                status = 406
        else:
            result = "Please provide a data character >= 4"
            error = True
            status = 406
        return {"result": result, "error": error}, status


def convert_to_base64(string):
    return base64.b64encode(string.encode("ascii"))


def check_padding(b64_string):
    if len(b64_string) % 4 != 0:  # check if multiple of 4
        while len(b64_string) % 4 != 0:
            b64_string = b64_string + "="
        req_str = base64.b64decode(b64_string)
    else:
        req_str = base64.b64decode(b64_string)
    return req_str.decode("utf-8")


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
