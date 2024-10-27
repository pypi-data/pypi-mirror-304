from setuptools import setup, find_packages

setup(
    name='asmix', 
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Ilyass Asmix',
    author_email='ilyassvv@gmail.com',
    description='This is a library to check email Hotmail if is availabe, get instagram information by username, get reset of user instagram, check if email registered in instagram, And many more features that may be added soon.',
    long_description=open('readme.md').read(),  
    long_description_content_type='text/markdown',
    url='https://t.me/n1z1n',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)