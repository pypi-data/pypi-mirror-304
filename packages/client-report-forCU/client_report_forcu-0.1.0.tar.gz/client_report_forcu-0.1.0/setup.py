from setuptools import setup, find_packages

setup(
    name="client_report_forCU",
    version="0.1.0",
    description="Пакет для генерации отчётов о клиентах из CSV-файлов",
    author="Ruslan",
    author_email="r.khuseyinov@edu.centraluniversity.ru",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
)
