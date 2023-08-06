from typing import Any, Dict, List
import codecs
import os

from jinja2 import (
    Environment,
    PackageLoader,
    select_autoescape,
    Template,
    TemplateNotFound,
    TemplateError,
    TemplateRuntimeError,
)

from lupin_danquin.core.application import Application
from lupin_danquin.core.tools.utils import die, info


class Val3Documentation:
    USR_APP_DIR = "usrapp"

    def _find_usrapp_dir(self) -> str:
        """Find the usrapp directory"""
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            if self.USR_APP_DIR in dirnames:
                return os.path.join(dirpath, self.USR_APP_DIR)
        die(msg=f"'{self.USR_APP_DIR}' directory not found")

    def _get_informations_from_applications(
        self, application_names: List
    ) -> List[Dict[str, Any]]:
        """Get all informations from applications"""

        apps_information = []
        base_program_path = self._find_usrapp_dir() + os.sep
        print(f"base_program_path: {base_program_path}")
        for application_name in application_names:
            program_path = base_program_path + application_name
            apps_information.append(
                Application(
                    program_path, application_name
                ).get_all_information_from_app()
            )
        return apps_information

    def _read_begining_of_file(self) -> str:
        with codecs.open(
            "lupin_danquin/assets/BeginingOfFile.md", encoding="utf-8"
        ) as f:
            result = f.read()
        return result

    def _read_end_of_file(self) -> str:
        with codecs.open("lupin_danquin/assets/EndOfFile.md", encoding="utf-8") as f:
            result = f.read()
        return result

    def _get_local_template(self) -> Template:
        try:
            # Create jinja2 environment
            env = Environment(
                loader=PackageLoader("lupin_danquin", "templates"),
                autoescape=select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            # Charge template
            template = env.get_template("val3_documentation_md.j2")
            return template
        except TemplateNotFound:
            die(
                msg="Template 'lupin_danquin/templates/val3_documentation_md.j2 not found"
            )

    def generate_markdown(self, applications_list: List) -> None:
        """Generate the documentation"""
        info(msg="Get informations from VAL3 applications")
        context = {
            "begining_of_file": self._read_begining_of_file(),
            "end_of_file": self._read_end_of_file(),
            "applications": self._get_informations_from_applications(applications_list),
        }

        template = self._get_local_template()
        try:
            content = template.render(context)
        except (TemplateError, TemplateRuntimeError) as e:
            die(msg=f"Error rendering Jinja2 template: {e}")

        with codecs.open(
            "lupin_danquin/val3_documentation.md", "w", encoding="utf-8"
        ) as f:
            f.write(content)
        info(msg="Documentation generated")
