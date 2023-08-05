from setuptools import *
import TimeShow.checkPythonVersion as check

check.checkPython312_or_Later()
check.checkPython37_or_earlier()

setup(
    name="TimeShow",
    version="2023.1.9",
    author="Siyuan",
    author_email="yuanbaoge@outlook.com",
    python_requires=">=3.8", 
    packages=find_packages(),
    install_requires=[
       'PyQt6>=6.4.0',
       'spyder>=5.3.0'
   ],
    classifiers = [
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: MacOS X :: Cocoa',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: User Interfaces'
    ]
)
