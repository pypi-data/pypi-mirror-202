from setuptools import setup, find_packages

VERSION ='0.0.2'

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Operating System :: Unix',
  'Operating System :: MacOS :: MacOS X',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
setup(
  name='admath1',
  version=VERSION,
  description='maths library with some intermediate and advanced function',
  long_description=open('README.txt').read() + '\n\n',
  url='', 
  author='Subhash Kumar',
  author_email='subhashfreelancer2004@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  install_requires=[''],
  packages=find_packages(),
  keywords=['maths','advance math','math','math formula','formula'], 
  
)
