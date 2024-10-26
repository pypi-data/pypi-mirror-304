import setuptools

setuptools.setup(
    name="odyssey_exchange_api",
    version="0.0.3",
    author="goduni",
    url="https://github.com/Odyssey-Trade/python-odyssey-exchange-api",
    description="Library for working with odyssey.trade",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("odyssey_exchange_api"),
    package_dir={"": "odyssey_exchange_api"},
    python_requires=">=3.10",
    install_requires=open("requirements.txt").read().splitlines(),
    license="MIT"
)
