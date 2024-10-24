from setuptools import setup, find_packages

setup(
    name="sparta-airflow-timetables",
    version="0.1.0",
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
    entry_points={
        "airflow.plugins": [
            "sparta_timetable_plugin = sparta_timetable_plugin.SpartaTimetablePlugin",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
