from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='infinitesimals',
    version='0.0.6',
    description='A capable HyperReal class and related methods for work with infinitesimals and nonstandard analysis.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Lyam Boylan',
    author_email='lyamboylan@gmail.com',
    license='MIT',
    keywords=['math', 'infinitesimal', 'infinitesimals', 'hyperreal', 'analysis', 'nonstandard analysis'],
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['numpy', 'scipy']
)