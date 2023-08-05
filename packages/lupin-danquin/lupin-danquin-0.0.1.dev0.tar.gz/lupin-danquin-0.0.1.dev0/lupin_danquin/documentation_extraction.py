import os

from core.application import Application
from core.external_resources import read_begining_of_file, read_end_of_file
from core.tools.utils import configure_logging, die
from core.val3_doc_generator.val3_doc_generator import Val3Documentation


APPLICATION_NAMES = [
    "TaskManager",
    "Watchdog",
]
USR_APP_DIR = "usrapp"


def find_usrapp_dir() -> str:
    """Find the usrapp directory"""
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        if USR_APP_DIR in dirnames:
            return os.path.join(dirpath, USR_APP_DIR)
    die(msg=f"'{USR_APP_DIR}' directory not found")


def get_informations_from_applications() -> list:
    """Get all informations from applications"""

    apps_information = []
    base_program_path = find_usrapp_dir() + os.sep

    for application_name in APPLICATION_NAMES:
        program_path = base_program_path + application_name
        apps_information.append(
            Application(program_path, application_name).get_all_information_from_app()
        )

    return apps_information


def main() -> None:
    """Main function"""

    configure_logging()

    context = {
        "begining_of_file": read_begining_of_file(),
        "end_of_file": read_end_of_file(),
        "applications": get_informations_from_applications(),
    }

    Val3Documentation().generate_markdown(context=context)


if __name__ == "__main__":
    main()
