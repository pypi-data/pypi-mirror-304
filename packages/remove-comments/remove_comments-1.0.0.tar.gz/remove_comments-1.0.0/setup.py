from setuptools import setup, find_packages

setup(
    name="remove_comments",  # Имя вашей библиотеки на PyPI
    version="1.0.0",  # Версия вашей библиотеки
    author="Ваше Имя",
    author_email="ваш_email@example.com",
    description="A Python library to remove hash comments from code files",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ваш_логин/remove_comments",  # URL на ваш репозиторий (например, на GitHub)
    packages=find_packages(),  # Поиск всех пакетов в каталоге
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
