from typing import Optional

from dotenv import load_dotenv
import typer

from lupin_danquin.core.tools.utils import (
    configure_logging,
    convert_application_name_to_list,
    must_get_string_value_from_env_var,
)
from lupin_danquin.core.val3_doc_generator.val3_doc_generator import Val3Documentation
from lupin_danquin.__init__ import __version__


load_dotenv()


cli = typer.Typer()


@cli.command(help="Print version")
def version():
    print(f"Version: {__version__}")


@cli.command()
def valdocs(
    application_names: Optional[str] = typer.Argument(
        ...,
        help="Name of applications to be documented. Ex: 'app1,app2,app3'",
        envvar="VAL3_APPLICATIONS",
    )
):
    """
    Generate documentation from VAL3 applications in usrapp directory.
    You can specify the applications to be documented in the 'danq valdocs' command
    or by setting the VAL3_APPLICATIONS environment variable.
    :param application_names: Name of applications to be documented. Ex: app1,app2,app3
    :type application_names: str

    :example: danq valdocs "App1,App2"
    """
    if not application_names:
        application_names = must_get_string_value_from_env_var("VAL3_APPLICATIONS")

    configure_logging()
    applications_list = convert_application_name_to_list(application_names)
    Val3Documentation().generate_markdown(applications_list=applications_list)
