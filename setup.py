from setuptools import setup, find_packages

setup(
    name='rustoredl',
    version="0.1.0",
    description='Downloads an Android application by given package name from RuStore',
    py_modules=['rustoredl'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rustoredl = rustoredl:main'
        ]
    },
    install_requires=[
        'requests==2.31.0',
        'tqdm==4.66.2'
    ]
)