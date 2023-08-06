import setuptools

setuptools.setup (
  include_package_data = True, 
  name='mycalc0001',
  version='0.0.1',
  description='oss-dev my calculator 0001',
  author='leeseunggeun',
  author_email='dss06023@gmail.com',
  url = "https://github.com/dss06023/calc0001",
  download_url = "https://github.com/dss06023/calc0001/archive/refs/tags/v0.0.1.zip",
  install_requires=['pytest'],
packages = ['mycalc']
  classifiers=[
      "Programmming Language :: Python :: 3",
  ],
)
