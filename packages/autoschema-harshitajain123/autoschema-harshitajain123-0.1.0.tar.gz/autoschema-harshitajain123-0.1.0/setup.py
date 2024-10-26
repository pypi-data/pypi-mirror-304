from setuptools import setup, find_packages

setup(
    name='autoschema-harshitajain123',
    version='0.1.0',
    description='A package that automates schema migrations by comparing schemas and generating migration scripts.',
    author='Harshita Jain',
    packages=find_packages(),  # Finds the autoschema package
    install_requires=[
        'SQLAlchemy',  # Add more dependencies if needed
    ],
    entry_points={
        'console_scripts': [
            'autoschema-migrate=autoschema.main:AutoSchemaMigrator',  # Command line entry point
        ],
    },
)
