from setuptools import setup, find_packages

setup(
    name="configchronicles",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "GitPython==3.1.24",
        'pytz',
    ],
)