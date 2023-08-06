from setuptools import setup, find_packages

setup(
    name="vhdx_2_zvol",
    version="0.1",
    description="Convert from vhdx to qcow to zvol",
    packages=find_packages(),
    install_requires=[],
    entry_points={"console_scripts": ["vhdx2zvol=main:main"]},
)
