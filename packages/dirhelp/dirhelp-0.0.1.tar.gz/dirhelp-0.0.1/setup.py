from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8'
]
 
setup(
  name='dirhelp',
  version='0.0.1',
  description='Dir Helping Library For Simplifying Your Work',
  long_description=open('README').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Monil Darediya',
  author_email='monildarediya1@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='dir-organise', 
  packages=find_packages(),
  install_requires=['colorama'] 
)
