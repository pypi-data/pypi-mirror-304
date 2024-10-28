from setuptools import setup, find_packages

setup(
    name='pip_cli_pack',
    version='0.0.1',
    author='Antonio Gavaldo',
    author_email='antonio.gavaldo@gmal.com',
    description='A simple CLI tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pick_cli=pick_cli.main:main',  # Command name and function to call
        ],
    },
)
