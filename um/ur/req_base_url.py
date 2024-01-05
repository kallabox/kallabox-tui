from os import environ


class MissingEnvVariable(Exception):
    pass  # Creating a new child class of exception


def req_get_base_url() -> str:
    """Function that returns the base url from the env variable or raises an exception if not found"""
    try:
        base_url = environ.get("KALLABOX_BASE_URL")

        if base_url is None:
            raise MissingEnvVariable("Requested Environment Varaible not found")

        return str(base_url)

    except KeyError:
        raise MissingEnvVariable("Requested Environment Variable not found")
