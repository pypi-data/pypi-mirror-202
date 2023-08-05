from setuptools import setup, find_packages


setup(
    name='web3_checksum',
    version='1.0',
    license='MIT',
    author="Xavier Rodriguez",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/boyiboy557111/web3_checksum',
    keywords='web3 checksum',
    install_requires=[
          'requests', 'web3',
      ],

)