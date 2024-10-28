"""
setup
"""
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sperrylabelimg',
    version='1.2.1.5',
    description='A GUI for labelling images customized for usage at Sperry Rail',
    author='Brooklyn Germa',
    author_email='brooklyn.germa@sperryrail.com',
    url='https://gitlab.com/bGerma/customlabelimg',
    license='MIT',
    packages=find_packages(),
    py_modules=["sperryLabelImg"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
    include_package_data=True,
    include_dirs=True,
    entry_points='''
        [console_scripts]
        sperrylabelimg=app:main
    ''',
)
