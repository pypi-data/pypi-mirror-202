from setuptools import setup, find_packages

setup(
    name='extotype',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'sphinx',
        'llama-index'
    ],
    classifiers=[],
    package_data={
        'extotype': [
            'static/extotype.js',
            'templates/search.html',
        ]
    },
)
