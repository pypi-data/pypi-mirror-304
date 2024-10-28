from setuptools import setup, find_packages

setup(
    name="pkg-vers",
    version="0.1.1",
    packages=find_packages(),
    author='Charles Feinn',
    author_email='chuckfinca@gmail.com',
    description="Easily extract and install packages necessary to run Python scripts and Jupyter notebooks.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chuckfinca/pkg_vers',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'nbformat',
        'stdlib-list'
    ],
    python_requires='>=3.8',
    license_files = ('LICENSE.txt',),
)
