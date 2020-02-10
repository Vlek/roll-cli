from setuptools import setup, find_packages

setup(
    name='roll',
    version='0.0.1',
    packages=['roll'],
    install_requires=['parsley>=1.3', 'click>=7.0'],
    entry_points={
        'console_scripts': [
            'roll = roll:roll'
        ]
    },
    url='https://github.com/vlek/roll',
    license='MIT',
    author='Derek (Vlek) McCammond',
    author_email='dmm545@drexel.edu',
    description='CLI-based dice roller',
    keywords='dnd roll dice die rp rpg game gaming cli terminal'
)
