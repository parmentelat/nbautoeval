# -*- coding: utf-8 -*-

# As a side note, I also have a simple tool for collecting corrections
# and publish them in pdf format.
# This is what the @BEG@ / @END@ thingy is for, just ignore this for now


# importing the ExerciseFunction class
from nbautoeval import ExerciseFunction, Args
from nbautoeval import CallRenderer, PPrintRenderer


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
    result_renderer=PPrintRenderer(width=20),
)



#
# an alternative exercise instance to demonstrate
# how to tweak the way the various columns are rendered
# an ExerciseFunction instance can provide:
# 
# * call_renderer: how to display the call (leftmost column)
# * result_renderer: how to display the results (2 middle columns)
# 
# the former should be some instance of one of the *CallRenderer classes
#   as defined in call.py
# the latter shoud be some instance of any of the *Renderer classes
#   as defined in renderer.py
# 
exo_percentages2 = ExerciseFunction(
    percentages, inputs_percentages,
    # show function name in leftmost column
    call_renderer=CallRenderer(show_function=False),
    # use pprint to format results
    result_renderer=PPrintRenderer(width=20),
)

#
# illustration on how to set fonts sizes
exo_percentages3 = ExerciseFunction(
    percentages, inputs_percentages,
    result_renderer=PPrintRenderer(width=20),
    # here
    font_size="75%",
    header_font_size="200%",
)
