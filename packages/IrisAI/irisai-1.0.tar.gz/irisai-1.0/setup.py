from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r', encoding="UTF-8") as f:
    return f.read()


setup(
  name='IrisAI',
  version='1.0',
  author='Tes',
  author_email='dev@tesnpe.ru',
  description='IrisAI API Connector',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='IrisAI',
  python_requires='>=3.12'
)