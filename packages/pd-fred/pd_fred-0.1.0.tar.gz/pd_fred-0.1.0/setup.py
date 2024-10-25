from setuptools import setup, find_packages

setup(
    name='pd_fred',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Python package to calculate Probability of Default using FRED data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pd_fred',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'fredapi>=0.4',
        'scipy>=1.5.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
