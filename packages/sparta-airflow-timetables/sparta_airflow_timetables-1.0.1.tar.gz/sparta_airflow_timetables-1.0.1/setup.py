from setuptools import setup, find_packages

setup(
    name="sparta-airflow-timetables",
    version="1.0.1",
    description="Airflow timetable plugin for Anbima and B3 holidays",
    author="Henrique Gomes Nunes",
    author_email="henrique.gomes@sparta.com.br",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pendulum",
        "pandas",
        "apache-airflow>=2.0",
    ],
    package_data={
        "sparta_airflow_timetables": ["anbima_holidays.csv", "b3pregao_holidays.csv"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
