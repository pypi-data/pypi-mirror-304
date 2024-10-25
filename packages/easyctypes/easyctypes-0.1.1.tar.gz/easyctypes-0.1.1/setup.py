from setuptools import setup, find_packages

setup(
    name='easyctypes',
    version='0.1.1',
    description='A ctypes-based module for advanced mouse control and device access',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ftnick/easyctypes',
    author='ftnick',
    author_email='',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
