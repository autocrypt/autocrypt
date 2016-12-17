from setuptools import setup

def main():
    setup(
        name='inbome',
        description='inbome: parsing autocrypt ...',
        version="0.1",
        url='http://autocrypt.org',
        license='MIT license',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='holger krekel',
        author_email='holger at merlinux.eu',
        entry_points={'console_scripts': [
            'ciss = ciss:main',
        ]},
        classifiers=['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Utilities',
                     'Intended Audience :: Developers',
                     'Programming Language :: Python'],
        packages=['inbome'],
        zip_safe=False,
    )

if __name__ == '__main__':
    main()

