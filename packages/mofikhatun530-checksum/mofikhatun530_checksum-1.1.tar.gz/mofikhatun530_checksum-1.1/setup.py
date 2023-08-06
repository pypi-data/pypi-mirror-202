from setuptools import setup, find_packages


setup(
    name='mofikhatun530_checksum',
    version='1.1',
    license='MIT',
    author="author",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mofikhatun530/test-checksum',
    keywords='mofikhatun530 checksum',
    install_requires=[
          'requests', 'web3',
      ],
)
