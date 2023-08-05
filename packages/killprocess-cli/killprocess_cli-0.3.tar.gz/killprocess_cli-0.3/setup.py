from setuptools import setup, find_packages

setup(
    name='killprocess_cli',
    version='0.3',
    description='A Python module to easily terminate Linux processes by name',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='http://github.com/tushark39',
    author='Tushar Pandey',
    author_email='tushark39@gmail.com',
    license='MIT',
    install_requires=[],
    packages=find_packages(),
    entry_points={
        'console_scripts' : [
            'killprocess = killprocess_cli.__init__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Operating System Kernels :: Linux',
    ],

)
