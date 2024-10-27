from setuptools import setup, find_packages

setup(
    name="receipt-generator-owttsair",
    version="0.1",
    description="A package for generating receipts from order data in JSON format",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "receipt-generator=receipt_generator.__main__:main",
        ],
    },
)
