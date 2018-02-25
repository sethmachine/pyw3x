from setuptools import setup

setup(name='pyw3x',
      version='0.1',
      description='Python utilities to manipulate Warcraft map files.',
      url='https://github.com/sethmachine/pyw3x',
      author='sethmachine',
      author_email='sethmachine01@gmail.com',
      license='MIT',
      install_requires=['psutil==5.4.3'],
      packages=['pyw3x'],
      # package_dir={'org.mitre.nlp.mbv':'org/mitre/nlp/mbv'},
      package_data={'pyw3x':['data/storm/*.*', 'data/storm/win-64/*.*']},
      zip_safe=False)

