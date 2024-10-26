from setuptools import setup

setup(
    name='invoice_generator_231231232',
    version='0.1.1',
    description='A package to generate invoices from order data.',
    author='Vlad',
    author_email='abvvladivanov@gmail.com',
    entry_points={
        'console_scripts': [
            'invoice_creator=invoice_creator.invoice_creator:main',
        ],
    },
    install_requires=[],
)
