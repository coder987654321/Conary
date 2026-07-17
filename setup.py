from setuptools import setup

setup(
    name="conary",
    version="2.0.0",
    py_modules=["conary"],
    entry_points={
        "console_scripts": [
            "conary=conary:main_cli"
        ]
    }
)