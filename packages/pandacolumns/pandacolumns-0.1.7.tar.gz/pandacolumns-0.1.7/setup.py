from setuptools import setup

setup(
    name='pandacolumns',
    version='0.1.7',
    description='Easily work with the pandas dataframes with an interactive interface',
    author='Asif Syed',
    license='MIT',
    packages=['pandacolumns'],
    install_requires=[
        'pandas',
'ipywidgets',
'IPython'
    ]
)
