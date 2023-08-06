from setuptools import setup, find_packages

setup(
    name="enprog",
    version="0.0.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "enprog=ENPROG.__main__:main",
        ]
    },
    python_requires=">=3.9, <=3.9.6",
    install_requires=[],
    author="Locutusque",
    author_email="locutusque.airshpcraft@gmail.com",
    description="A programming language with english-like syntax",
    license="MIT",
    url="https://github.com/Locutusque/EnProg/tree/Python-Variant",
)

