from flask import Flask, request
import base64
import json


def configure_routes(app):
    @app.route("/calculus")
    def calculus():
        query = request.args.get("query")
        if len(query) >= 4:
            checked_query = check_padding(query)
            try:
                result = eval(checked_query)
                if isfloat(result):
                    status = 200
                else:
                    result = "Error with your input: " + query
                    status = 406
            except:
                result = "Error with your input: " + query
                status = 406
        else:
            result = "Please provide a data character >= 4"
            status = 406
        return {"result": result, "status": status}, status


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
