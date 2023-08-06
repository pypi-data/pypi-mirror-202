from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='processplatform',
  version='1.0.3',
  data_files=[('processplatform/bin', ['processplatform/bin/get_process.exe'])],
  description='Computer process information',
  long_description="Get any computer information or python plugins path with a simple get command.",
  url='https://google.com',
  author='vesper',
  author_email='google@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='process',
  packages=find_packages(),
  install_requires=[]
)