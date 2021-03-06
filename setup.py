from setuptools import setup, find_packages
import platform

settings = dict(
    name='fs_ops',
    packages=find_packages(),
    version='0.0.5',
    description='Basic fs operations on stupid windows.',
    long_description='Long description.',
    author='MatteoLacki',
    author_email='matteo.lacki@gmail.com',
    url='https://github.com/MatteoLacki/fs_ops.git',
    keywords=['Great module', 'Devel Inside'],
    classifiers=['Development Status :: 1 - Planning',
                 'License :: OSI Approved :: BSD License',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering :: Chemistry',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7'],
    # install_requires=['checksumdir', 'flask'],
    install_requires=['flask'],
    scripts = ["bin/grep_paths.py",
               "bin/msync.py"])

setup(**settings)