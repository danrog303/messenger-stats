import os

base_dir = os.path.dirname(os.path.realpath(__file__))

tests_config = {
    "FRONTEND_SERVICE_URL": "http://localhost:3000",
    "BACKEND_SERVICE_URL": "http://localhost:8080",
    "STATS_SERVICE_URL": "http://localhost:2137",

    "TEST_FILE_PATH": os.path.join(base_dir, "fb-files.zip")
}
