from setuptools import setup, find_packages

setup(
    name="mypackage_den",  # Уникальное имя пакета
    version="0.1.0",  # Версия пакета
    author="Кузнецов Денис Михайлович",
    author_email="kdm.01082002@mail.ru",
    description="Пакет, демонстрирующий работу с декораторами, дескрипторами, итераторами и генераторами",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
