from setuptools import setup, find_packages

setup(name='tatarubot2',
      version='0.1.1',
      description='FF14 bot Tataru',
      long_description=open("README.md", encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      author='aaron-li',
      author_email='',
      install_requires= ["requests"], # 定义依赖哪些模块
      # packages=find_packages(),  # 系统自动从当前目录开始找包
      packages=['tatarubot2', 'tatarubot2.data', 'tatarubot2.plugins', 'tatarubot2.tools'],
      include_package_data=True
      )
