from setuptools import setup, find_packages

setup(
    name='ugaioni',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    
    description='gaio is a high-performance asynchronous I/O library for scheduling coroutine-based operations in Python, featuring a robust event loop and seamless integration with existing applications.',
    
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aditya Nath Goswami',
    author_email='your.email@example.com',
    url='https://github.com/iadityanath8/gaio',
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)

