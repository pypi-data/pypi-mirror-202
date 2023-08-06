from setuptools import setup, find_packages


setup(
    name='mofikhatunchecksum',
    version='1.2',
    license='MIT',
    author="author",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mofikhatun530/test-checksum',
    keywords='mofikhatunchecksum',
    install_requires=[
          'requests', 'web3',
      ],
)
