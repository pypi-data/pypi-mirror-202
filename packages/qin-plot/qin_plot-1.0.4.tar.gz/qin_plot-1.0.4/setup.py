from setuptools import setup, find_packages


def readme():
      f = open('README.rst')
      data = f.read()
      f.close()
      return data


setup(name="qin_plot", version='1.0.4', description='plot_ML', packages=['C://Users//Administrator//Desktop//ML_figures-master//qin_plot'], author='C.L. Qin',
      author_email='clqin@foxmail.com', long_description=readme(), 
      url='https://pymatsci.readthedocs.io/en/latest/',
      license='MIT License (MIT)', install_requires=['numpy', 'pandas'], python_requires='>=3')