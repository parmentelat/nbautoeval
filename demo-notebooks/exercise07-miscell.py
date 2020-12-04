# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   notebookname: Not limited to functions
#   version: '1.0'
# ---

# %% [markdown]
# <span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat&nbsp;<img src="../media/inria-25.png" style="display:inline"></span><br/>

# %%
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")


# %% [markdown]
# # Not limited to functions

# %% [markdown]
# It is pretty straightforward to use this for checking python objects that are not functions per-se, by defining closure functions that can be passed to the framework. See e.g. the `inconnue` exercise in flotpython.

# %% [markdown]
# # Copying input data

# %% [markdown]
# One important aspect to keep in mind if you deal with functions that do side effects on their input arguments - which is something that can be part of the requirements.
#
# In general, the frameork needs to **copy all input data**, otherwise the student- and teacher-provided functions would mess in each other's space, and that cannot end well.
#
# This is the purpose of the `copy_mode` flag, which by default is 'deep' which means deep copy, but it is sometimes useful to use other methods.
#

# %% [markdown]
# # Tweaking the way things are displayed

# %% [markdown]
# Taking the case of `ExerciseFunction` which is a representative example, here's how the rendering works:
#
# * the `exercise` instance has 2 renderers :
#   * `exercise.call_renderer` (see file `callrenderer.py`)
#   * `exercise.result_renderer` (see file `renderer.py`)
# * when showing the line corresponding to one function call, i.e. one `Args` instance that I call, say, `args`:
#   * for the leftmost column  
#     `exercise.call_renderer.render(call)` is called and is expected to produce a `Rendered` object; in this context `call` is a `Call` instance that contains `args` - as well as the function called;
#   * for the *expected/obtained* columns  
#     `exercise.result_renderer.render(result)` is called with the results returned by the official or the student code
#
# `Rendered` allows to carry text, math, code, CSS classes and properties, so all in all this is pretty flexible.

# %% [markdown]
# ##### Example with and without `show_function`

# %% [markdown]
# Defining an `ExerciseFunction` with a CallRenderer that has `show_function=False` will cause a slightly different output, in an attempt to save space.

# %%
def curve(a, b, c=12): 
    # make it work only when a==b
    return a ** 2 + 3 * a * b + c + (a - b)


# %%
# the default is to display the function name in 1st column
from exercises.curve import exo_curve
exo_curve.correction(curve)

# %%
# see the source file below to see how to obtain that presentation
from exercises.curve import exo_curve_noname
exo_curve_noname.correction(curve)

# %%
from listing import listing
listing("../exercises/curve.py")

# %% [markdown]
# # display numpy arrays as images

# %% [markdown]
# at this point this is primarily a prototype

# %%
from exercises.checkers import exo_checkers
exo_checkers.example(1)

# %%
import numpy as np

def checkers(n):
    ...

def checkers1(n):
    I, J = np.indices((n, n))
    return (I+J) % 2

def checkers2(n):
    I, J = np.indices((n, n))
    return (I+J+1) % 2


# %%
exo_checkers.correction(checkers)

# %%
exo_checkers.correction(checkers1)

# %%
exo_checkers.correction(checkers2)

# %%
from listing import listing
listing("../exercises/checkers.py")

# %% [markdown]
# # long args

# %%
from exercises.longargs import exo_longargs
exo_longargs.example()


# %%
def longargs(x):
    return len(x) %2 == 0


# %%
exo_longargs.correction(longargs)

# %% [markdown]
# ***
