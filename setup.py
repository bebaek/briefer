from setuptools import find_packages, setup

setup(
    name='briefer',
    version='0.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'briefer = briefer.briefer:main',
        ],
    },
)
