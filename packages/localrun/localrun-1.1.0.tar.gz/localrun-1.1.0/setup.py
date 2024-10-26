from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='localrun',
    version='1.1.0',
    description='A simple local server to run your Python applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MrFidal',  
    author_email='mrfidal@proton.me',  
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'localrun=localrun.server:main',
        ],
    },
    python_requires='>=3.6',
    keywords='local server, Python applications, development server, web server',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
)
