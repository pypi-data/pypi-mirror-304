from setuptools import setup, find_packages

setup(
    name='simplesocket-py',  # Replace with your package name
    version='0.1.0',  # Initial version
    author='Helio',
    author_email='helio.m.s.l.2012@gmail.com',
    description='A port of the NPM package "SimpleSocket" (https://www.npmjs.com/package/simple-socket-js)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NullClock/simplesocket-py',  # Replace with your repository URL
    packages=find_packages(),  # Automatically find packages in your module
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust based on your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',  # Specify the Python version required
)