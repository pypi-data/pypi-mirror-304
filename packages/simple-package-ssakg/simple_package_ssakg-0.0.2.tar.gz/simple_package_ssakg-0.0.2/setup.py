from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

setup(
    name='simple_package_ssakg',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy~=2.1.2'],
    url='',
    license='',
    author='Przemysław Stokłosa',
    author_email='przemyslaw.stoklosa@gmail.com',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['python', 'first package'],
    python_requires='>=3.11',
)
