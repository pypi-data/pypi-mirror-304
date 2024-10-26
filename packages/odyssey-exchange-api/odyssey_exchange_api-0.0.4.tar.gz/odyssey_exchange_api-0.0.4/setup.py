import setuptools

setuptools.setup(
    name="odyssey_exchange_api",
    version="0.0.4",
    author="goduni",
    url="https://github.com/Odyssey-Trade/python-odyssey-exchange-api",
    description="Library for working with odyssey.trade",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("odyssey_exchange_api"),
    package_dir={"": "odyssey_exchange_api"},
    python_requires=">=3.10",
    install_requires=[
        "pydantic==2.9.2",
        "httpx==0.27.2",
        "websockets==13.1"
    ],
    license="MIT"
)
