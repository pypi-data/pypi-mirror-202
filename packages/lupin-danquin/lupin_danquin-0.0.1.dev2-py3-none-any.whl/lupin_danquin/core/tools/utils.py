from typing import List
import logging
import os
import re
import sys


def must_get_string_value_from_env_var(var_name: str):
    """Get a string value from an environment variable.
    Args:
        var_name (str): The name of the environment variable.
    Returns:
        str: The value of the environment variable.
    Logs:
        Error: If the environment {var_name} variable is not set.
        sys.exit(1)
    """
    if not os.getenv(var_name):
        logging.error(f"Environment variable {var_name} is not set.")
        sys.exit(1)
    return os.getenv(var_name)


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )


def die(msg: str) -> None:
    logging.error(msg)
    sys.exit(1)


def info(msg: str) -> None:
    logging.info(msg)


def get_version():
    """get version from setup.cfg file and
    update __version__ in lupin_danquin.__init__.py
    """
    with open("setup.cfg", "r", encoding="utf-8") as f:
        setup_cfg = f.read()
    print(setup_cfg)
    _version = re.search(
        r"(^version = )(\d{1,2}\.\d{1,2}\.\d{1,2})(\.[a-z]{1,})?(\d{1,2})?",
        setup_cfg,
        re.MULTILINE,
    )
    version = ""
    for group in _version.group(2, 3, 4):
        if group is not None:
            version = version + str(group)
    content = f'__version__ = "{version}"\n'

    with open("lupin_danquin/__init__.py", "w", encoding="utf-8") as outfile:
        outfile.write(content)
    return version


def convert_application_name_to_list(application_name: str) -> List:
    """Convert application name to list.
    Args:
        application_name (str): The name of the application.
    Returns:
        list: The list of the application name.
    """
    return [app.strip() for app in application_name.split(",") if app.strip()]
