from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dragonxxdlib',
  version='1.0.0',
  description='Download from tik tok and youtube and facebook and other soon',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='yassen waly',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='Download from tiktok and youtube and facebook', 
  packages=find_packages(),
  install_requires=[''] 
)