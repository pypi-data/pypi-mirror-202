from setuptools import setup

setup(
    name="solid-broccoli",
    version="0.0.1",
    install_requires=[
        "python-dateutil",
    ],
    author="IM-coding",
    # IN bash just type hello-world
    entry_points={
        "console_scripts": [
            "solid-broccoli = solid_broccoli.convert:unix_to_human_and_versa",
        ]
    },
)
