import os.path

from setuptools import setup, find_packages
import codecs

c_dir = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(c_dir, "README.md"), encoding='utf-8') as ld:
    long_description = "\n" + ld.read()

VERNUM = '0.0.3'
DESC = 'Encapsulating game server and client into one package'

setup(
    name='pyclient2d',
    version=VERNUM,
    author="Jopat2409",
    author_email="joantpat@gmail.com",
    url="https://github.com/Jopat2409/pyclient2d",
    description=DESC,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'game', 'client', 'server', 'engine'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)
