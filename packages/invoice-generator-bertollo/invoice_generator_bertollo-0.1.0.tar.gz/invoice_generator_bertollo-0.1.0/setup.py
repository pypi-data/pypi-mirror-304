from setuptools import setup, find_packages

setup(
    name='invoice_generator_bertollo',
    version='0.1.0',
    description='A package to generate invoices from JSON order data.',
    author='Victor Bertollo',
    author_email='bertollo.victor@gmail.com',
    packages=['invoice_generator'],
    entry_points={
        'console_scripts': [
            'generate_invoice = invoice_generator.__main__:main',
        ],
    },
)
