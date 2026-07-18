from setuptools import setup

setup(
    name="conary",
    version="2.1.0b1",
    py_modules=["conary"],
    entry_points={
        "console_scripts": [
            "conary=conary:main_cli"
        ]
    }
)