import setuptools

setuptools.setup(
    name="odyssey_exchange_api",
    version="0.0.2",
    author="goduni",
    description="Library for working with odyssey.trade",
    packages=[
        "odyssey_exchange_api",
        "odyssey_exchange_api.clients",
        "odyssey_exchange_api.enums",
        "odyssey_exchange_api.exceptions",
        "odyssey_exchange_api.objects",
        "odyssey_exchange_api.requests",
        "odyssey_exchange_api.responses",
        "odyssey_exchange_api.utils"
    ],
    python_requires=">=3.10"
)
