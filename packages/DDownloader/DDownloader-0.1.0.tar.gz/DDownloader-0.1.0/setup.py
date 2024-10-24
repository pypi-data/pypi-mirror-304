from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='DDownloader',
    version='0.1.0',
    description='A library to download HLS and DASH manifests and decrypt media files.',
    author='Pari Malam',
    author_email='shafiqsamsuri@serasi.tech',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    package_data={
        '': ['bin/*'],
    },
    entry_points={
        'console_scripts': [
            'd-downloader = manifest_downloader:main',
        ],
    },
)