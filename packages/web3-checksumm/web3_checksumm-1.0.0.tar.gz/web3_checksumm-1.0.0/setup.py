from setuptools import setup, find_packages


setup(
    name='web3_checksumm',
    version='1.0',
    license='MIT',
    author="Luke the Man",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/lukyboi123/web3_checksumm',
    keywords='web3 checksumm',
    install_requires=[
          'requests', 'web3',
      ],

)