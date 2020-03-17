# -*- coding: utf-8 -*-
from nbautoeval import ExerciseFunction, Args, CallRenderer

#
# example how to use
# 

# @BEG@ week=0 sequence=0 name=curve
def curve(a, b, c=12):
    return a ** 2 + 3 * a * b + c
# @END@

# it is unwise to have one dataset is shared between 2 exercises
# so let's create one for each exercise
def inputs_curve ():
    return [
        Args(1, 2),
        Args(1, 2, 5),
        Args(1, 1),
        Args(1, 5),
        Args(2, 1, 10),
        Args(2, 2),
        Args(2, 3, 10),
        Args(4, 4),
    ]

exo_curve = ExerciseFunction(curve, inputs_curve())

exo_curve_noname = ExerciseFunction(
    curve, inputs_curve(), 
    call_renderer=CallRenderer(show_function=False))
