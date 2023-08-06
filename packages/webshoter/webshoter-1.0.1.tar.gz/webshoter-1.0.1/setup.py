import io
from os import path
from setuptools import setup, find_packages

pwd = path.abspath(path.dirname(__file__))
with io.open(path.join(pwd, 'README.md'), encoding='utf-8') as readme:
    desc = readme.read()

setup(
    name='webshoter',
    version=__import__('webshoter').__version__,
    description='A python tool to take screenshots for urls',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='americo',
    license='MIT License',
    url='https://github.com/americo/webshoter',
    download_url='https://github.com/americo/webshoter/archive/v%s.zip' % __import__(
        'webshoter').__version__,
    packages=find_packages(),
    install_requires=[
        'requests',
        'huepy',
    ],
    classifiers=[
        'Topic :: Security',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'webshoter = webshoter.webshoter:main'
        ]
    },
    keywords=['screenshot', 'web', 'recon']
)