from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Operating System :: Unix',
  'Operating System :: MacOS :: MacOS X',
  'Operating System :: Microsoft :: Windows :: Windows 10'
]
 
setup(
  name='IOTELLME',
  version='0.0.9',
  description='A very basic IOTELLME',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='IOTELLME LLC',
  author_email='iotellme@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['IOTELLME','Token','Send','Read','Write1'],
  packages=find_packages(),
  install_requires=["requests","jsons"] 
  )
