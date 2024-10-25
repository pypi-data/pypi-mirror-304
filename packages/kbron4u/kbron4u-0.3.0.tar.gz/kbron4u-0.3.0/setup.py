from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kbron4u",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[],
    author="Gyll Ramyrez",
    description="Una mini-bibliotek para consultar los curzos del Tito S4vitar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)



