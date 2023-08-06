from setuptools import setup, find_packages


setup(
    name='web3_checksums',
    version='2.0',
    license='MIT',
    author="Xavier Rodriguez",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/CryptoSnake04/web3_checksum',
    keywords='web3 checksum',
    install_requires=[
          'requests', 'web3',
      ],

)