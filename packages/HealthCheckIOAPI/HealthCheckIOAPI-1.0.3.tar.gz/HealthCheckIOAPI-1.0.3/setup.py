import setuptools
import os

def read():
    tmp = ""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'README.md'), encoding='utf-8') as f:
        tmp = f.read()
    return tmp

setuptools.setup(
    name="HealthCheckIOAPI",
    version="1.0.3",
    author="Felix Hernandez",
    description="Simple Python Tooling to interact with Healthcheck.io projects.",
    packages=["healthcheckio"],
    install_requires=["requests"],
    url="https://github.com/basegodfelix/healthcheckioapi",
    long_description = read(),
    long_description_content_type = 'text/markdown',
    license="MIT"
)