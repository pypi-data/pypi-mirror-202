from setuptools import setup, find_packages

setup(
    name="B0tHe1Per_test_api",
    version="0.5",
    author="Serj",
    author_email="buda_serj@yahoo.com",
    description="Test API for Bot Helper project",
    url='https://github.com/serjbuda/B0tHe1Per.git',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bot_helper = B0tHe1Per_test_api.bot_interface:main',
            'bot_notes = B0tHe1Per_test_api.notes_main:main_note_book'
        ]
    },
    package_data={'B0tHe1Per_test_api': ['file_sorter.py', 'notes_classes.py']},
    include_package_data=True
)
