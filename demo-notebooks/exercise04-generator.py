# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed
#     cell_metadata_json: true
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# # A sample generator exercise

# %%
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")

# %% [markdown]
# ## usual generator

# %% [markdown]
# `nbautoeval` has some provisions for dealing with generator functions; assume you ask students to write a generator that iterates over the n first integer squares, like e.g. :
#
# ```python
# def squares(n):
#     for i in range(n):
#         yield n**2
# ```

# %% [markdown]
# for dealing with this situation, you would create an instance of `ExerciseGenerator`; such an instance is created from
#
# * the solution (e.g. here the `squares` generator)
# * a list of inputs, each expressed as a `GeneratorArgs` instance
#
# the latter is similar to a regular `Args` instance, in that it describes the parameters to pass to the function; and in addition, `GeneratorArgs` allows to describe primarily how many times the generator needs to be triggered, and which of these results need to be taken into account; this is done through an *islice* attribute, a tuple whose (max. 3) pieces behave like the parameters to `range()` - or `islice()`
#
# let us see this on a first example

# %%
# as you can see, we display a list of the yielded values
# which is maybe not optimal

from exercises.squares import exo_squares
exo_squares.example()


# %% [markdown]
# Not that these examples are very realistic, but they intend to illustrate that mechanism :
#
# 1. first example has no *islice* set, so the generator obtained via `squares(2)` is triggered until its end, which amounts to 2 values
# 1. second example, `GeneratorArgs` is created with `islice=(1, 4)`; thus the generator is triggered 4 times, and only the last three results are displayed (and compared)
# 1. third example : `islice=(5,)`, meaning 5 runs; here the generator expires before that, it's fine, we just keep the 3 values
# 1. fourth example, the range (2, 8, 3) contains indices 2 and 5, so we only consider these runs; it is enough for the student code to coincide only on these 2 runs 
#

# %%
# a wrong answer
def squares(n):
    return (i**2 for i in range(n) if i<=5)


# %%
exo_squares.correction(squares)


# %%
# a right answer
def squares(n):
    return (i**2 for i in range(n))


# %%
exo_squares.correction(squares)

# %% [markdown]
# ****

# %% [markdown]
# ## same with a limit
#
# when the requested generator does not end, it is tedious to have to create an *islice* for each and every dataset (test row), so it can be convenient to define the exercise instance with a global limit on the number of iterations. 
#
# here the exercise instance is here created with `max_iterations = 5`; it means that the framework will always stop after 5 iterations; the examples below try to illustrate the interaction of that setting with various *islice* settings.

# %%
from exercises.squares import exo_squares_maxed
exo_squares_maxed.example()


# %%
# always the same student correct code

def squares(n):
    return (i**2 for i in range(n))


# %%
# which displays this 
exo_squares_maxed.correction(squares)

# %% [markdown]
# ****

# %% [markdown]
# ## checking for types w/ an infinite iterator

# %% [markdown]
# Suppose we create an `ExerciseGenerator` from the standard (itertools) `count()` generator, with `max_iterations = 5`

# %%
from exercises.squares import exo_count_maxed

exo_count_maxed.example()


# %%
# which could be in most cases approximated with 
# that is fine because it is still an iterator
def mycount_ok():
    return range(1000)


# %%
exo_count_maxed.correction(mycount_ok)


# %%
# but this one is wrong, it returs a list, so:
def mycount_ko():
    return list(range(10))


# %%
exo_count_maxed.correction(mycount_ko)

# %% [markdown]
# ****

# %% [markdown]
# ***

# %%
from listing import listing
listing("../exercises/squares.py")

# %% [markdown]
# ***
# ***
# ***
#

# %% [markdown]
# # iterating on prime numbers

# %% [markdown]
# ### with `max_iterations`

# %% [markdown]
# It may be prudent to set a `max_iterations` on the exercise instance to avoid endless loops.

# %%
from exercises.primes import exo_primes
exo_primes.example()

# %% [markdown]
# ### without `max_iterations`

# %% [markdown]
# **this is not working** 
# see issue #4

# %%
#from exercises.primes import exo_primes_no_limit
#exo_primes_no_limit.example()

# %%
listing("../exercises/primes.py")

# %% [markdown]
# ***

# %% [markdown]
# ### passing iterators as arguments to iterators

# %% [markdown]
# **BEWARE** that this feature is experimental; in 0.6.2 we had to explicitly tag the exercise with `copy_mode="tee"` for it to work properly; setting this flag on other gen-based exos, including `primes` above, tends to break things.

# %% [markdown]
# Objective here is to write an iterator that takes an iterator as argument, and iterates its derivative, i.e. the difference between consecutive terms.

# %% [markdown]
# This is currently very patchy and could use a second pass; the logic is kind of OK, including for cloning iterators
#
# However rendering an argument iterator in the 'Appel' column remains to be done, right now it is still totally unedible ;)

# %%
from exercises.differential import exo_differential

exo_differential.example()

# %%
# it's far from clear from this table, but we run differential on 
# (*) itertools.count() so the expected output is a constant 1
# (*) squares() that iterates 0, 1, 4, 9, 16 ... 
#     so the expected outcome of differential is 1, 3, 5, 7, ..

from exercises.differential import differential
exo_differential.correction(differential)

# %%
listing("../exercises/differential.py")
