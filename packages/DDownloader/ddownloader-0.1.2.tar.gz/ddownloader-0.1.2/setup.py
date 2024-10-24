from setuptools import setup, find_packages

setup(
    name='DDownloader',
    version='0.1.2',
    description='A library to download HLS and DASH manifests and decrypt media files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
)