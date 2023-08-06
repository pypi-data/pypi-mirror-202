import setuptools
import os

def read():
    tmp = ""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'README.md'), encoding='utf-8') as f:
        tmp = f.read()
    return tmp

setuptools.setup(
    name="Felog",
    version="1.0.1",
    author="Felix Hernandez",
    description="Felog is yet another simple logging library to quickly and simply deploy logging with projects.",
    packages=["felog"],
    # install_requires=["logging"],
    url="https://github.com/basegodfelix/felog",
    long_description = read(),
    long_description_content_type = 'text/markdown',
    license="MIT"
)