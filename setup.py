from setuptools import find_packages, setup

import versioneer

setup(
    cmdclass=versioneer.get_cmdclass(),
    name="lens_db",
    packages=find_packages(),
    version=versioneer.get_version(),
)
