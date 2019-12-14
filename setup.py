from setuptools import find_packages, setup

setup(
    name='briefer',
    version='0.0.0',
    python_requires='>3.6',
    packages=find_packages(),
    package_data={
        '': ['templates/*.html'],
    },
    install_requires=[
        'cryptography',
        'jinja2',
        'pytz',
        'requests',
        'ruamel.yaml',
        'tzlocal',
    ],
    entry_points={
        'console_scripts': [
            'briefer = briefer.main:main',
        ],
    },
)
