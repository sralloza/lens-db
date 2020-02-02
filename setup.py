import sys
from pathlib import Path

from setuptools import find_packages, setup

version = Path(__file__).with_name("lens_db").joinpath("VERSION").read_text()
requirements = Path(__file__).with_name("requirements.txt").read_text().splitlines()


setup(
    name="lens_db",
    url="https://github.com/sralloza/lens-db.git",
    description="Lens database manager",
    version=version,
    author="Diego Alloza",
    entry_points={"console_scripts": ["lens-db=lens_db.src.main:main"]},
    include_package_data=True,
    author_email="lens-db.support@sralloza.es",
    packages=find_packages(),
    install_requires=requirements,
    # package_data={'aes.test': ['test_data/ensure_filepath/*']},
    package_data={"lens_db": ["VERSION"]},
    tests_require=["pytest"],
    zip_safe=False,
)
