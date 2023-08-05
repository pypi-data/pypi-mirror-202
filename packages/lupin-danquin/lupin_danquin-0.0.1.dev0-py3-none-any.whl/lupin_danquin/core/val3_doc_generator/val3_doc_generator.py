import codecs

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
    Template,
    TemplateNotFound,
    TemplateError,
    TemplateRuntimeError,
)

from core.tools.utils import die


class Val3Documentation:
    def _get_local_template(self) -> Template:
        try:
            # Create jinja2 environment
            env = Environment(
                loader=FileSystemLoader("lupin_danquin/templates"),
                autoescape=select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            # Charge template
            template = env.get_template("val3_documentation_md.j2")
            return template
        except TemplateNotFound:
            print(
                "Template 'lupin_danquin/templates/val3_documentation_md.j2 not found"
            )

    def generate_markdown(self, context={}) -> None:
        """Generate the documentation"""
        template = self._get_local_template()
        try:
            content = template.render(context)
        except (TemplateError, TemplateRuntimeError) as e:
            die(msg=f"Error rendering Jinja2 template: {e}")

        with codecs.open(
            "lupin_danquin/val3_documentation.md", "w", encoding="utf-8"
        ) as f:
            f.write(content)
