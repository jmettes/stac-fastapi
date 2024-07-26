from setuptools import setup

install_requires = [
    "stac-fastapi.api==2.5.5",
    "stac-fastapi.extensions",
    "stac-fastapi.types",
    "uvicorn",
    "attr",
    "shapely",
    "tiledb",
    "pystac==1.10.0"
]

setup(
    name="stac-fastapi.tiledb",
    description="An implementation of STAC API based on the FastAPI framework.",
    install_requires=install_requires,
    entry_points={"console_scripts": ["stac-fastapi-tiledb=stac_fastapi.tiledb.app:run"]},
)