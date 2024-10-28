from setuptools import setup, find_packages

setup(
    name='sduplayground',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'playwright',
        'pytesseract',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'sduplayground=sduplayground.main:main',
        ],
    },
)