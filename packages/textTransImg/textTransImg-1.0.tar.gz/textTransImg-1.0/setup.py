from distutils.core import setup
import setuptools

packages = ['textTransImg']  # 唯一的包名，自己取名
setup(name='textTransImg',
      version='1.0',
      author='hh',
      packages=packages,
      package_dir={'requests': 'requests'}, )
