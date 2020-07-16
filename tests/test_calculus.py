from ..app import calculus
from flask import url_for


def test_calculus(client):
    assert client.get(url_for("calculus")).status_code == 200

