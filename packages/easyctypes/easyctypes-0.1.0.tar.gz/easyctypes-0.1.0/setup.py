from setuptools import setup, find_packages

setup(
    name='easyctypes',
    version='0.1.0',
    description='A ctypes-based module for advanced mouse control and device access',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ftnick/easyctypes',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
