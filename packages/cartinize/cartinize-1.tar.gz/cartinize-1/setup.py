from setuptools import setup, find_packages

VERSION = '1'
DESCRIPTION = 'Cartinese translator'

setup(
    name="cartinize",
    version=VERSION,
    author="ktkv419 (Kutikov Pasha)",
    author_email="<kutikovpasha@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    keywords=['python', 'string', 'translate', 'carti', 'slatt'],
)
