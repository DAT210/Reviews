from setuptools import find_packages, setup

setup(
    name='reviews',
    version='1.0.0',
    maintainer='Group 3',
    description='The review API built with the flask framework.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    exstras_require={
        'test': [
            'unittest',
        ],
    },
)