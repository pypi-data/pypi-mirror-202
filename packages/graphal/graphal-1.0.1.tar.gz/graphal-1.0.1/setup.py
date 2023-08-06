from setuptools import setup, find_packages

setup(
    name='graphal',
    version='1.0.1',
    author='graphal',
    description='Graphs & Algorithms',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='graphal python',
    python_requires='>=3.7'
)
