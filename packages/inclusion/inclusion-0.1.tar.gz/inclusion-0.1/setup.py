from setuptools import setup, find_packages

setup(
    name='inclusion',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'inclusion=inclusion.cli:main',
        ],
    },
    package_data={
        'inclusion': ['list.txt'],  
    },
    description='A tool to check for file inclusion vulnerabilities.',
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',  
    author='MrFidal',
    author_email='mrfidal@proton.me',
    url='https://github.com/ByteBreach/inclusion',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
