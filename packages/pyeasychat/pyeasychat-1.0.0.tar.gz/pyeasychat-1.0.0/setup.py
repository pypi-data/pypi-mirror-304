from setuptools import setup, find_packages

setup(
    name="pyeasychat",              # Имя библиотеки
    version="1.0.0",                # Версия
    packages=find_packages(),       # Автоматический поиск пакетов в проекте
    description="A simple chat library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="boryagames",
    author_email="gyu1242ru@gmail.com.email@example.com",
    url="https://www.boryagames.ru",  # Ссылка на мой сайт
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",        # Минимальная версия Python
)
