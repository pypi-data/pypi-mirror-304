from setuptools import setup

setup(
    name='pycloudkit',
    version='1.0.1',
    packages=['pycloudkit'],
    author='griguchaev',
    author_email='griguchaev@yandex.ru',
    description='A library for creating and working with cloud databases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/professionsalincpp/pyserver',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)