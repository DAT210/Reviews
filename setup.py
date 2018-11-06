from setuptools import find_packages, setup

setup(
    name='reviews',
    version='1.0.0',
    maintainer='Group 3 - Ole & Tien',
    description='The review API built with the flask framework.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'Requests',
        'MySQL-connector-python',
        'click',
        'python-dotenv',
    ],
    exstras_require={
        'test': [
            'unittest',
        ],
    },
)