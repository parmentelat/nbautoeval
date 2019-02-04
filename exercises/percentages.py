# -*- coding: utf-8 -*-

# As a side note, I also have a simple tool for collecting corrections
# and publish them in pdf format.
# This is what the @BEG@ / @END@ thingy is for, just ignore this for now


# importing the ExerciseFunction class
from nbautoeval.exercise_function import ExerciseFunction

# the Args object is for defining inputs 
from nbautoeval.args import Args


#
# this is a regular Python module, so I can define
# any variable, here a global that I need in this context
# 
nucleotides = 'CAGT'



########## step 1
# You need to define the 'correct' function
# i.e. one that would be accepted as valid for the problem

# @BEG@ name=percentages
def percentages(adn):
    "calcule des percentages de CAGT dans un adn"
    total = len(adn)
    return {
        nucleotide : len([p for p in adn if p == nucleotide])*100./total
        for nucleotide in nucleotides
    }
# @END@



########## step 2
# You need to provide datasets
# This is expected to be a list of Args instances
# each one describes all the arguments to be passed
# to the function
# in this particular case we define 2 input sets, so
# the correction will have 2 meaningful rows
#
inputs_percentages = [
    Args('ACGTACGA'),
    Args('ACGTACGATCGATCGATGCTCGTTGCTCGTAGCGCT'),
]

# The Args object takes eactly the arguments to be passed to the function
# so if the function was expecting 2 arguments, then I would have added
# Args(10, 12)
# or even
# Args(10, *(12, 13, 14))



########## step 3
# finally we create the exercise object
# NOTE: this is the only name that should be imported from this module
#
exo_percentages = ExerciseFunction(
    # first argument is the 'correct' function
    # it is recommended to use the same name as in the notebook, as the
    # python function name is used in HTML rendering 
    percentages,
    # the inputs
    inputs_percentages,
    # the rest is optional, it contains  various tweaks
    # on how to display input arguments
    layout='pprint',
    # in particular here, the widths of the first 3 columns in the correction table
    layout_args=(40, 25, 25),
)
