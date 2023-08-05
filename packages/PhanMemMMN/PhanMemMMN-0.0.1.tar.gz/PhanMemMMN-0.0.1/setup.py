from setuptools import setup

setup(
    name='PhanMemMMN',
    version='0.0.1',
    author='ViDat',
    author_email='tiendatopip@gmail.com',
    description='A music player package for Linux',
    py_modules=['MusicApp'],
    install_requires=[
        'pygame',
        'numpy',
        'Pillow',
        'customtkinter',

    ],
)