import setuptools

setuptools.setup(
    name='notebook-logger',
    version='0.1.0',
    license='Apache-2.0',
    author='Daniel Lee',
    author_email='rootuser.kr@gmail.com',
    description='Simple logger for jupyter notebook user',
    long_description=open('README.md').read(),
    url='https://github.com/asulikeit/notebook-logger',
    packages=['notebook_logger'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ]
)