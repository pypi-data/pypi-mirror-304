from setuptools import setup
from setuptools.config.expand import entry_points

setup(
    name='generate_receipt_elf_unic',
    description='module that creates receipt',
    version='0.1.0',
    py_modules=['generate_receipt'],

    entry_points={
        'console_scripts':
            ['generate_receipt = generate_receipt:main']
    },

    author='Varvara',
    python_requires='>=3.6',
)

