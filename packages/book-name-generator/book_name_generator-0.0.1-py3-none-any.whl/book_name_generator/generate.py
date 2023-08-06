"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = book_name_generator.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
import random

from book_name_generator import __version__

__author__ = "Levi Eby"
__copyright__ = "Levi Eby"
__license__ = "MIT"

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from book_name_generator.skeleton import fib`,
# when using this Python module as a library.


# the (somenting) of (something)
beginnings = [
    'Abyss', 'Angel', 'Assassin', 'Blade', 'Blood', 'Castle', 
    'Cavern', 'Captain', 'Chariot', 'Chasm', 'City', 'Cloud', 
    'Crossroads', 'Crown', 'Curse', 'Demons', 'Desert', 
    'Empire', 'Eye', 'Fires', 'Flame', 'Forest', 'Gate', 
    'Guardian', 'Heart', 'Heir', 'Horn', 'Hour', 'Hunt', 
    'King', 'Kingdom', 'Kingdom', 'Knife', 'Legend', 
    'Lord', 'Memory', 'Oath', 'Path', 'Prince', 'Princess', 
    'Prophecy', 'Protectors', 'Queen', 'Raven', 'Rhythm', 
    'Ring', 'River', 'Sanctuary', 'Scroll', 'Serpent', 
    'Shadow', 'Shield', 'Shroud', 'Spirit', 'Storm', 
    'Thieves', 'Tomb', 'Towers', 'Valley', 'Voyage', 
    'Warrior', 'Wanderer', 'Wheel', 'Whisper', 'Wings', 'Word']

endings = [
    'Anger', 'Ash', 'Chaos', 'Crystal', 'Daggers', 'Darkness', 
    'Dawn', 'Deceit', 'Descent', 'Destruction', 'Dreams', 
    'Dusk', 'Enchantment', 'Eternity', 'Exile', 'Fire', 
    'Fools', 'Glass', 'Glory', 'Gold', 'Heaven', 'Honor', 
    'Ice', 'Lies', 'Light', 'Magic', 'Majesty', 'Memory', 
    'Midnight', 'Mystery', 'Secrets', 'Smoke', 'Stone', 
    'Swords', 'Time', 'Truth', 'Twilight', 'War', 'Winter', 
    'the Dragon', 'the Earth', 'the Traitor', 'the World'
]

def generate(bookNum):
    i1 = int(bookNum / endings.__len__())
    i2 = bookNum % endings.__len__()
    return f"The {beginnings[i1]} of {endings[i2]}"

def generate_random():
    rand_num = random.randint(0, endings.__len__() * beginnings.__len__())
    return generate(rand_num), rand_num

def main():
    while True:
        name, num = generate_random()
        print(f"Book: {num}:\t {name}", end = "")
        if input("").lower() in ['quit', 'exit', 'done', 'x']:
            break

if __name__ == "__main__":
    main()