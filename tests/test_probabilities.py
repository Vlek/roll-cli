#!/usr/bin/env python3
"""Test the probabilities of dice rolls.

In this sequence of tests, we will be figuring out whether the dice
rolls fit roughly with expected probabilistic ranges.

For instance, if we roll a 1d20, then we would expect all numbers
within the 1-20 range of values to have an equal chance of appearing.
This is however not the case when we start adding modifiers or rolling
multiple dice. 2d20 does not give equal probabilities to all numbers
within the range 2-40, it instead turns into a bell curve with 21
being the most common number at a 5% chance and all others higher and
lower having a lesser degree of chance at 0.25% intervals.

In order to test these rough probabilities, I will be using the
website https://anydice.com/ as they have a nicely done out graph
system for visualizing as well as the ability to export the numbers
into an easy-to-consume format.
"""
