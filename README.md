[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/Vlek/roll.svg?branch=master)](https://travis-ci.org/Vlek/roll)
[![codecov](https://codecov.io/gh/Vlek/roll/branch/master/graph/badge.svg)](https://codecov.io/gh/Vlek/roll)
![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2Fvlek%2Froll)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://perso.crans.org/besson/LICENSE.html)

<!-- Project Logo/Header -->
<p align="center"><img src="https://user-images.githubusercontent.com/15008772/110541742-02522e00-80dd-11eb-944c-367bb3380cf9.png" width="80"/></p>
<h3 align="center">PyRoll</h3>
<p align="center">A CLI dice roller with all of the bells and whistles!</p>

<!-- Table of Contents -->
<h3>Table of Contents</h3>
<ol>
  <li>
    <a href="#about">About</a>
    <ul>
      <li><a href="#built-with">Built With</a></li>
    </ul>
  </li>
  <li>
    <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
    </ul>
    <ul>
      <li><a href="#installation">Installation</a></li>
    </ul>
  </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </li>
</ol>

# About

Dice roller CLI Script

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!
        
## Built With

This project is made using the [Python](https://www.python.org) language with dependencies:
- [Poetry](https://python-poetry.org/)
- [Pyparsing](https://github.com/pyparsing/pyparsing/)
- [Click](https://click.palletsprojects.com/en/7.x/)

# Getting Started

## Prerequisites

Please ensure that Python is installed:
```sudo apt-get install python python3-pip```

## Installation

Currently not available via PyPi. :(

If you are interesting in previewing, please `git clone` the repo and then `python -m pip install .`

# Usage

    roll <nothing>      - Rolls 1d20

    roll <expression>   - Rolls all dice + does math

Expressions:

    1d20                - Rolls one 20-sided die

    d20                 - Does not require a '1' in front of 'd'

    d%                  - Rolls 1d100

    d8 + 3d6 + 5        - Rolls 1d8, 3d6, and adds everything together

    (1d4)d6             - Rolls 1d4 d6 die
    
    1dpi                - Rolls 1dπ
    
    5!                  - Evaluates 5 factorial
    
    64 % 1d7            - Evaluates the modulus division of what is rolled from 1d7

# Contributing

This is just a fun puzzle for me right now, so I am not looking for help. If there is a feature that you believe should be added, please create an issue with as much info as you can give me (examples are helpful!)

# License

This project is licensed under GPLv3.
