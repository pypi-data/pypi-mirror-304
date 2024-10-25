from setuptools import setup, find_packages
import os

def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name='beautifull_terminal',
    version='1.5',
    long_description = read_readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    description='Automatically beautify your terminal output with colors.',
    author='starcrusher2025',
    url='https://github.com/StarGames2025/beautifull_terminal',
    install_requires=[],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

#python setup.py sdist bdist_wheel
#twine upload dist/*