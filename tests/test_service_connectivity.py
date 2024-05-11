import requests
from test_config import tests_config


def test_frontend_connectivity():
    result = requests.get(tests_config["FRONTEND_SERVICE_URL"])
    assert "html" in result.text
    assert result.status_code == 200


def test_backend_connectivity():
    result = requests.get(tests_config["BACKEND_SERVICE_URL"])
    assert result.status_code == 404


def test_stats_connectivity():
    result = requests.get(tests_config["STATS_SERVICE_URL"])
    assert result.status_code == 404
