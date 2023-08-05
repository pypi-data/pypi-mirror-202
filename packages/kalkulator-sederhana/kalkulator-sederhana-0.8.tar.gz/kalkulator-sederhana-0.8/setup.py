from setuptools import setup, find_packages


setup(
    name='kalkulator-sederhana',
    version='0.8',
    license='MIT',
    author="Sopyan Syauri",
    author_email='rifai.sopyan04@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/sopyansyauri/module/tree/master/kalkulator-sederhana',
    keywords='example project',
    install_requires=[
          'numpy',
      ],

)