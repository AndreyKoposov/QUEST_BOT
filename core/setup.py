from setuptools import setup

setup(
    name='core',
    version='0.1.0',
    description='Core package',
    packages=['game', 'utils', 'mongo', 'storage'],
    install_requires=[
        'redis',
        'motor'
    ],
)
