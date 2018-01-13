from setuptools import setup

setup(name='hivewe',
      version='0.1',
      description='Python interface to manipulating Warcraft III map files.',
      url='https://github.com/sethmachine/hive-world-editor',
      author='sethmachine',
      author_email='sethmachine01@gmail.com',
      license='MIT',
      install_requires=['psutil==5.4.3'],
      packages=['hivewe'],
      # package_dir={'org.mitre.nlp.mbv':'org/mitre/nlp/mbv'},
      package_data={'hivewe':['data/storm/*.*', 'data/storm/win-64/*.*']},
      zip_safe=False)

