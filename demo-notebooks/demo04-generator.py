# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## A sample generator exercise

# %%
# %load_ext autoreload
# %autoreload 2

# %%
# just so that it runs smoothly under binder
import sys
sys.path.insert(0, '..')

# %% [markdown]
# ## usual generator

# %%
from exercises.squares import exo_squares
exo_squares.example()


# %%
def squares(n):
    return (i**2 for i in range(n))


# %%
exo_squares.correction(squares)

# %% [markdown]
# ****

# %% [markdown]
# ## same with a limit
#
# the exercise instance is here created with `max_iterations = 5`

# %%
from exercises.squares import exo_squares_maxed
exo_squares_maxed.example()


# %%
def squares(n):
    return (i**2 for i in range(n))


# %%
exo_squares_maxed.correction(squares)

# %% [markdown]
# ****

# %% [markdown]
# ## checking for types w/ an infinite iterator

# %% [markdown]
# standard `count()` with a limit on the number of iterations (max_iterations = 5)

# %%
from exercises.squares import exo_count_maxed

exo_count_maxed.example()


# %%
def mycount1():
    return range(1000)


# %%
exo_count_maxed.correction(mycount1)

# %%
import itertools

def mycount2():
    return itertools.count()


# %%
exo_count_maxed.correction(mycount2)


# %%
def mycount3():
    return list(range(10))


# %%
exo_count_maxed.correction(mycount3)

# %% [markdown]
# ****

# %% [markdown] {"trusted": true}
# ## infinite iterators

# %%
from exercises.squares import exo_squares_count_maxed

# %%
exo_squares_count_maxed.example()


# %%
def squares_count1():
    for n in itertools.count():
        yield n**2


# %%
exo_squares_count_maxed.correction(squares_count1)


# %%
def squares_count2():
    return (n**2 for n in itertools.count())


# %%
exo_squares_count_maxed.correction(squares_count2)

# %% [markdown]
# ***

# %%
# !cat ../exercises/squares.py

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
# !cat ../exercises/primes.py

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
# !cat ../exercises/differential.py
