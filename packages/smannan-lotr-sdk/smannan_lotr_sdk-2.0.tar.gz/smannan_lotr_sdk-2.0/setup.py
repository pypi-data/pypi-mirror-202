from setuptools import setup, find_packages


setup(
    name='smannan_lotr_sdk',
    version='2.0',
    author="Sonia Mannan",
    author_email='smannan95@hotmail.com',
    packages=find_packages('.'),
    package_dir={'': '.'},
    url='https://github.com/smannan/lotr_sdk',
    keywords='sdk, python',
    install_requires=[
      'logging',
      'os',
      'requests',
      'sys'
    ],

)