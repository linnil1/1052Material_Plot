from setuptools import setup

setup(name='materialdiagram',
      version='1.0',
      description='Plot diagram for simple materials.',
      url='https://github.com/linnil1/1052Material_Plot',
      author='linnil1',
      license='GPLv3',
      packages=['materialdiagram'],
      install_requires=[
          'sympy',
          'matplotlib',
          'IPython',
          'jupyter'
      ],
      zip_safe=False)
