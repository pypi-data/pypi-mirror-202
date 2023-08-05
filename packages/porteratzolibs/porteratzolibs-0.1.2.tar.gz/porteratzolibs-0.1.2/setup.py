import setuptools
from setuptools import setup

setup(
    name='porteratzolibs',
    version='0.1.2',    
    description='Collection of utils',
    url='https://github.com/porteratzo/porteratzolibs',
    author='Omar Montoya',
    author_email='omar.alfonso.montoya@hotmail.com',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['matplotlib',
                      'numpy', 
                      'open3d',
                      'pandas',
                      'opencv-python',                    
                      ],

    classifiers=[
        'Operating System :: POSIX :: Linux', 
        'Programming Language :: Python :: 3',
    ],
)