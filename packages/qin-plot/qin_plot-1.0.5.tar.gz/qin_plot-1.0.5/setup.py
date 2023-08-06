from setuptools import setup, find_packages


def readme():
      f = open('README.rst')
      data = f.read()
      f.close()
      return data


setup(name="qin_plot", version='1.0.5', description='plot_ML', packages=find_packages(), author='C.L. Qin',
      author_email='clqin@foxmail.com', long_description=readme(), 
      url='https://pymatsci.readthedocs.io/en/latest/',
      license='MIT License (MIT)', install_requires=['numpy', 'pandas'], python_requires='>=3')