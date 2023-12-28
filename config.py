from os import environ

service_token = environ.get("KALLABOX_SERVICE_TOKEN")
base_url = environ.get("KALLABOX_BASE_URL")


def get_base_url():
    return base_url


def get_service_token():
    return service_token
