from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='test_pipinstall_whp',
      version='0.0.3',
      description='test pip installation',
      author='haopengwu',
      author_email='wuhaopeng106@gmail.com',
      requires= ['numpy','matplotlib'],
      packages=find_packages(),
      license="apache 3.0"
      )
