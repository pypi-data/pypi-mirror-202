from setuptools import setup, find_packages

def install_requires():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

setup(
    name='extotype',
    version='0.6',
    packages=find_packages(),
    install_requires=install_requires(),
    classifiers=[],
    package_data={
        'extotype': [
            'static/extotype.js',
            'templates/search.html',
        ]
    },
)
