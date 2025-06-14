from setuptools import setup, find_packages

setup(
    name='options_pricer',
    version='0.1.0',
    description='A Python package for options pricing',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'pandas', 'matplotlib'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)