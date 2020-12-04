# -*- coding: utf-8 -*-
from nbautoeval import ExerciseFunction, Args, CallRenderer

#
# an exemple of hard-formatting of long strings
#

# @BEG@ week=0 sequence=0 name=longargs
def longargs(a):
    return ord(a[0]) % 2 == 0
# @END@

from string import ascii_uppercase as ABC
from itertools import cycle, islice

def longstr(length, start=0):
    return "".join(islice(cycle (ABC), start, start+length))

# it is unwise to have one dataset is shared between 2 exercises
# so let's create one for each exercise
def inputs_longargs ():
    return [ Args(longstr(10*n)) for n in range(1, 12)]

exo_longargs = ExerciseFunction(
    longargs, inputs_longargs(),
    nb_examples=0,
    call_renderer=CallRenderer(
        show_function=False,
        css_properties={'word-wrap': 'break-word', 'max-width': '20em'},
        ))
