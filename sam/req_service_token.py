from os import environ


class MissingEnvVariable(Exception):
    pass  # Creating a new child class of exception


def req_get_service_token() -> str:
    """Function that returns the service token from the env variable or raises an exception if not found"""
    try:
        service_token = environ.get("KALLABOX_SERVICE_TOKEN")

        if service_token is None:
            raise MissingEnvVariable("Requested Environment Variable not found")

        return str(service_token)

    except KeyError:
        raise MissingEnvVariable("Requested Environment Variable not found")
