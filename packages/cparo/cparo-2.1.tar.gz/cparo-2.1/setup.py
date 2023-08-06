from setuptools import setup

setup(
    name='cparo',
    version='2.1',
    packages=['cparo'],
    install_requires=[
        'requests',
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'cheaters=cheaters.main:main'
        ]
    }
)
