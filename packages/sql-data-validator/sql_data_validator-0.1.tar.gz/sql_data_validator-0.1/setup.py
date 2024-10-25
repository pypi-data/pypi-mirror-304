from setuptools import setup, find_packages

setup(
    name='sql_data_validator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.5.3',
        'numpy>=1.24.0',
    ],
    description='A package to validate SQL databases for data quality issues.',
    author='Your Name',
    author_email='mmanishssharma2@gmail.com',
    url='https://github.com/yourusername/sql_data_validator',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
