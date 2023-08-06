from setuptools import setup, find_packages

setup(
    name = "Gestor_CSprog87",
    version= "1.0.0",
    description="Gestor para una base de datos de clientes con fichero .csv",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Camilo Andres Sanabria - CSprog87",
    author_email="csmarketing.global@gmail.com",
    url="https://github.com/CSprog87",
    license_files=["LICENSE"],
    packages=find_packages(),
    scripts=["config.py", "database.py", "helpers.py", "menu.py", "run.py", "ui.py"],
    test_suite= "tests",
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()]     
    
)