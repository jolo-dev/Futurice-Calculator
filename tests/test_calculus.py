from routes.calculus import configure_routes, check_padding, convert_to_base64
from flask import url_for, Flask
import json
import pytest


@pytest.fixture
def client():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    return client


def test_check_padding_1(client):
    result = check_padding("MQ==")
    assert result == "1"


def test_check_padding_short(client):
    result = check_padding("MiAqICgyMy8oMyozKSktIDIzICogKDIqMyk")
    assert result == "2 * (23/(3*3))- 23 * (2*3)"


def test_check_padding_same_formula(client):
    result1 = check_padding("MiAqICgyMy8oMyozKSktIDIzICogKDIqMyk")
    result2 = check_padding("MiAqICgyMy8oMyozKSktIDIzICogKDIqMyk=")
    assert result1 == result2


def test_calculus_1_plus_1(client):
    response = client.get("/calculus?query=MSsx")
    mocked_result = {"result": 2, "status": 200}
    assert response.status_code == 200
    assert json.loads(response.get_data()) == mocked_result


def test_calculus_1(client):
    response = client.get("/calculus?query=MQ==")
    mocked_result = {"result": 1, "status": 200}
    assert response.status_code == 200
    assert json.loads(response.get_data()) == mocked_result


def test_calculus_failure(client):
    response = client.get("/calculus?query=A")
    mocked_result = {"result": "Please provide a data character >= 4", "status": 406}
    assert response.status_code == 406
    assert json.loads(response.get_data()) == mocked_result


def test_calculus_float(client):
    response = client.get("/calculus?query=MS8z")
    mocked_result = {"result": 0.3333333333333333, "status": 200}
    assert response.status_code == 200
    assert json.loads(response.get_data()) == mocked_result


def test_calculus_negative_float(client):
    response = client.get("/calculus?query=MiAqICgyMy8oMyozKSktIDIzICogKDIqMyk")
    mocked_result = {"result": -132.88888888888889, "status": 200}
    assert response.status_code == 200
    assert json.loads(response.get_data()) == mocked_result


def test_calculus_not_a_formula(client):
    response = client.get("/calculus?query=QUJDRA==")
    mocked_result = {"result": "Error with your input: QUJDRA==", "status": 406}
    assert response.status_code == 406
    assert json.loads(response.get_data()) == mocked_result


def test_convert_string_to_base64(client):
    b64_string = convert_to_base64("1")
    assert b64_string == b"MQ=="
