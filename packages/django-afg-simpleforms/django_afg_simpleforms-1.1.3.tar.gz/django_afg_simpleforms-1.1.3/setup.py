from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='django_afg_simpleforms',
  version='1.1.3',
  author='afguy',
  author_email='alwaysfrownguy@gmail.com',
  description='No description',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='django python forms',
  project_urls={
    'Documentation': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
  },
  python_requires='>=3.7'
)