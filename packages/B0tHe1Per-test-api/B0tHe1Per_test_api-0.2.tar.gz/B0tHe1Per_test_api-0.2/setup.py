from setuptools import setup, find_packages

setup(
    name="B0tHe1Per_test_api",
    version="0.2",
    author="Serj",
    author_email="buda_serj@yahoo.com",
    description="Test API for Bot Helper project",
    url='https://github.com/serjbuda/B0tHe1Per.git',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bot_helper = B0tHe1Per_test_api.bot_interface:main'
        ]
    }
)
