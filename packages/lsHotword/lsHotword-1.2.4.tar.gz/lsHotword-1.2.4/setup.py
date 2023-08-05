from setuptools import setup, find_packages
from os import path

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'lsHotword',
  packages = ['lsHotword'],
  version = '1.2.4',
  license='MIT',
  include_package_data=True,
  long_description=long_description,
  long_description_content_type='text/markdown',
  description = 'Hotword/Wake Word detection in python for all platforms(Windows/Linux/Mac).',
  author = 'Hemant Kumar',
  author_email = 'iamhemantindia@protonmail.com',
  url = 'https://github.com/HemantKArya/lsHotword',
  download_url = '',
  package_data={
        'lsHotword': ['*.wav'],
    },
  keywords = ['hotword', 'detector', 'lshotword','windows','python','wake word','wake-word','detection'],
  install_requires=[
          'matplotlib',
          'numpy',
          'pydub',
          'pyaudio',
          'tensorflow',
          'scipy',
          'pyqt6'
      ],
  entry_points={
        'console_scripts': ['lshTrainer = lsHotword.funcHTrainer:main',
                            'lshDatagen = lsHotword.funcHDatagen:main',
                            'lshTestModel = lsHotword.ls:HTest',
                            'lshUITrainer = lsHotword.uitrainer:main',
                            'lshModelTrainer = lsHotword.funcHfTrainModel:main']
    },
  classifiers=[],
)