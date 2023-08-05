import os

from core.application import Application


if __name__ == "__main__":
    base_program_path = (
        os.path.abspath(os.path.dirname(__file__) + r"/../../danquin/val3/usrapp/")
        + "/"
    )
    application_names = [
        "TaskManager",
    ]
    result = []
    for application_name in application_names:
        program_path = base_program_path + application_name
        app = Application(program_path, application_name)
        result += app.check_coding_rules()

    if len(result) > 0:
        print(f"{len(result)} errors found while checking coding rules:")
        print()
        print(
            """
        """.join(
                result
            )
        )
    else:
        print("No error found while checking coding rules.")
    exit(len(result))
