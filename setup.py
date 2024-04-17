from setuptools import setup, find_packages

with open("requirements.txt") as requirements:
    REQUIREMENTS = [r.strip() for r in requirements.readlines()]

setup(
    name='rustoredl',
    version="0.1.0",
    description='Downloads an Android application by given package name from RuStore',
    py_modules=['rustoredl', 'util'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rustoredl = rustoredl:main'
        ]
    },
    install_requires=REQUIREMENTS
)