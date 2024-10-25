from setuptools import setup, find_packages

setup(
    name="harbinger_vault_client",
    author="Moises Gaspar",
    author_email="moises.gaspar@testsieger.com",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.1,<3",
    ],
    license="MIT",
)
