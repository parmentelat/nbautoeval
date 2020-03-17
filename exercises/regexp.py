# -*- coding: utf-8 -*-
from nbautoeval import ExerciseRegexp, ExerciseRegexpGroups
from nbautoeval.args import Args

########## step 1
# one correct answer

# @BEG@ week=6 sequence=6 name=pythonid more=regexp
at_least_two = "TA(TA)+"
# @END@

########## step 2 : the datasets

# used for generating all orders
import itertools

germs = [ 'AGCT', 'CAGT', 'TATG', 'CGTA' ]

# building the inputs
inputs =  []
# one run will be made on this string as-is
inputs += ['AGCTTATATATACAGT']

# here we construct 24 strings by combining the 4 seeds above in all possible orders
inputs += [
    "".join(x) for x in itertools.permutations(germs)
    ]
# so this amounts to 25 different runs

########## step 3
exo_at_least_two = ExerciseRegexp(
    # for building a regexp we need to provide a name explicitly
    # (as opposed to when we deal with functions, that have an internal name)
    'at_least_two',
    # the pattern that describes the correct regexp
    at_least_two,
    # the datasets are, as always, a list of Args objects
    [Args(x) for x in inputs],
    # match_mode can be either 'match' or 'search', depending on
    match_mode = 'finditer',
    nb_examples = 8)

# XXX to be clarified again
at_least_two_ko = "TATA"
