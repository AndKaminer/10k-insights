from setuptools import find_packages, setup

setup(
    name="Fintech Lab Assignment",
    version="1.0",
    package_dir={"": "flaskr"},
    packages=find_packages(where="flaskr") + find_packages(where="flaskr/nonflask"),
    install_requires=[
        'flask',
        'flask-socketio',
        'anthropic',
        'nltk',
        'sec-downloader'
        ]
    )

