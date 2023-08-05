import logging
import re
import sys


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )


def die(msg: str) -> None:
    logging.error(msg)
    sys.exit(1)


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
