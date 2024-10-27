from setuptools import setup, find_packages

# Загрузка .egg на PyPI больше не поддерживается, поэтому загружаем wheel и sdist
def read(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

setup(
    name='finutils_scochilloff',
    version='0.1.1',
    long_description=read("README.md"),
    packages=find_packages(),
    install_requires=[],
)