from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='dragonmapper',
    version='0.1',
    author='Thomas Roten',
    author_email='thomas@roten.us',
    url='https://github.com/tsroten/dragonmapper',
    description=('Identification and conversion functions for Chinese'
                 'text processing'),
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
        'Topic :: Text Processing :: Linguistic',
        ],
    keywords=['chinese', 'mandarin', 'transcription', 'pinyin', 'zhuyin',
              'ipa', 'convert', 'bopomofo', 'hanzi', 'characters', 'readings'],
    packages=['dragonmapper', 'dragonmapper.data'],
    package_data={'dragonmapper': ['data/*.tsv', 'data/*.csv']},
    test_suite='dragonmapper.tests',
    install_requires=['zhon>=1.1.3'],
)
