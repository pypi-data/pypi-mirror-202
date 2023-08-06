from setuptools import find_packages
from setuptools import setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="jupyterhub-tmpnativeauthenticator",
    version="1.0.1",
    description="JupyterHub Native Authenticator with tmp login",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gorbacheb/tmpnativeauthenticator",
    author="Vladimir Nedugov",
    author_email="MegaRs1@yandex.ru",
    license="MIT",
    packages=find_packages(),
    install_requires=["jupyterhub>=1.3", "bcrypt", "onetimepass"],
    include_package_data=True,
)
