from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SimpleEngine',
  version='0.3',
  description='A simple game engine',
  long_description_content_type=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Gust Schadron',
  author_email='gustscd@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='game', 
  packages=find_packages(),
  install_requires=['pygame', 'pillow']
)