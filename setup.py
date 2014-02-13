from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='dragonmapper',
    version='0.1dev',
    author='Thomas Roten',
    author_email='thomas@roten.us',
    url='https://github.com/tsroten/dragonmapper',
    description='Converts to/from Chinese transcription systems',
    long_description=long_description,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        ],
    keywords=['chinese', 'mandarin', 'transcription', 'pinyin', 'zhuyin',
              'ipa', 'convert', 'bopomofo'],
    packages=['dragonmapper'],
    test_suite='dragonmapper.tests',
    install_requires=['zhon>=1.1.3'],
)
