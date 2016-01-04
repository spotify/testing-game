from setuptools import setup

setup(name='testinggame',
      version='1.0.0',
      description='A script for counting the number of tests per developer',
      url='http://github.com/spotify/testing-game',
      author='Will Sackfield',
      author_email='sackfield@spotify.com',
      license='Apache',
      packages=['testinggame'],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'testinggame = testinggame:_main'
        ]
      })