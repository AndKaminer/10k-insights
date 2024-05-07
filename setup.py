from setuptools import find_packages, setup

setup(
    name="Fintech Lab Assignment",
    version="1.0",
    package_dir={"": "flaskr"},
    packages=find_packages(where="flaskr") + find_packages(where="flaskr/nonflask"),
    install_requires=[
        'flask==3.0.3',
        'flask-socketio==5.3.6',
        'anthropic==0.25.7',
        'nltk==3.8.1',
        'sec-downloader==0.11.1',
        'bs4==0.0.2',
        'yfinance==0.2.38']
    )
