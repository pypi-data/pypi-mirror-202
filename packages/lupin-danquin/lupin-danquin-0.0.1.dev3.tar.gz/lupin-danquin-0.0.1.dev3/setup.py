from setuptools import setup


from lupin_danquin.core.tools.utils import get_version


if __name__ == '__main__':
    setup(
        version=get_version()
    )
