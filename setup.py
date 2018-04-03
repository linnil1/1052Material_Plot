from setuptools import setup

setup(name='materialdiagram',
      version='0.1',
      description='Plot diagram for simple materials.',
      url='https://github.com/linnil1/1052Material_Plot',
      author='linnil1',
      license='',
      packages=['materialdiagram'],
      install_requires=[
          'sympy',
          'matplotlib',
          'IPython',
          'jupyter'
      ],
      zip_safe=False)
