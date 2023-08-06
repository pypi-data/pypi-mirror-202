# 编写完包源码后，python setup.py sdist生成pip压缩包
# 解压压缩包，python setup.py install  安装自己的包，就可以引用了


from setuptools import find_packages
from distutils.core import setup

setup(name='wbtest_utils',  # 包名
      version='0.0.2',  # 版本号
      description='微博自动化测试工具',
      long_description='',
      author='zhihui18',
      author_email='zhihui18@staff.weibo.com',
      url='https://gitlab.weibo.cn/andarchitecture/Android_AutoTest',
      license='',
      install_requires=[],
      keywords='',
      packages=find_packages('src'),  # 必填
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )
