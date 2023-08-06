from setuptools import setup, find_packages


setup(
    name='mofikhatun530-checksum',
    version='1.0',
    license='MIT',
    author="Slava Ukraini",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mofikhatun530/test-checksum',
    keywords='mofikhatun530 checksum',
    install_requires=[
          'requests', 'web3',
      ],

)
