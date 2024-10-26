from setuptools import setup, find_packages

setup(
    name='ccdaviewer',
    version='0.1.0',
    author='Tanaka Chiromo',
    author_email='tanakachiromo@gmail.com',
    description='This is the python client to the API hosted by https://www.ccdaviewer.com',
    packages=find_packages(),
    install_requires=[
          'requests',
      ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)