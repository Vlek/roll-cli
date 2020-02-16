from setuptools import setup

setup(
    name='roll',
    version='0.3.0',
    packages=['roll'],
    install_requires=[
        'click>=7.0',
        'parsley>=1.3'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest>=5.3.5',
        'python-coveralls>=2.9.3'
    ],
    entry_points={
        'console_scripts': [
            'roll = roll.roll:roll_cli'
        ]
    },
    test_suite='tests',
    url='https://github.com/vlek/roll',
    license='MIT',
    author='Derek (Vlek) McCammond',
    author_email='dmm545@drexel.edu',
    description='CLI-based dice roller',
    keywords='dnd roll dice die rp rpg game gaming cli terminal'
)
