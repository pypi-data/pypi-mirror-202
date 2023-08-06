from setuptools import setup

from src.datamodelsFrontier import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

extra_test = [
    'pytest>=4',
    'pytest-cov>=2',
]

setup(
    name='datamodelsFrontier',
    version=__version__,
    description="Datamodels needed for Frontier API",

    author='THG-Frontier',
    author_email='DL-TechAPIGateway@thehutgroup.com',

    install_requires=['pydantic', ],
    extras_require={
        'dev': extra_test
    },

    py_modules=['datamodelsFrontier'],
    package_dir={"": "src"},

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

    long_description=long_description,
    long_description_content_type="text/markdown",
)
