from setuptools import setup, find_packages

setup(
    name="ip_fetcher_phillip_bridgeman",
    version="5.4",
    description="A Python utility to fetch the current machine's public IP address.",
    author="Phillip Bridgeman",
    author_email="your.email@example.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ipfetch=ip_fetcher.ip_parser_phillip_bridgeman:main',
        ],
    }
)
