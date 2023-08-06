import setuptools
from pathlib import Path

setuptools.setup(
    name="tarjimonlib",
    version="0.0.1",
    author="Olimov Behruz",
    author_email="olimovbehruz738@gmail.com",
    description="Ushbu kutubxona tarjima qilish uchun ishlatiladi",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)