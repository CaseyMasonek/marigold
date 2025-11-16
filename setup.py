from setuptools import setup, find_packages

setup(
    name="marigold",
    version="0.1",
    py_modules=["marigold"],
    packages=find_packages(),
    install_requires=["click","lark"],
    entry_points={
        "console_scripts": [
            "marigold = marigold.cli:main",
        ],
    },
)
