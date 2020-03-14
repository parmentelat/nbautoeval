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
#       jupytext_version: 1.1.7
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   notebookname: Functions with more arguments
#   version: '1.0'
# ---

# %% [markdown]
# <span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat&nbsp;<img src="../media/inria-25.png" style="display:inline"></span><br/>

# %%
# just so that it runs smoothly under binder
import sys
sys.path.append("..")

# %% [markdown]
# # Functions with more arguments

# %% [markdown]
# ## The `Args` object

# %% [markdown]
# The framework of course supports function calls with a higher number of arguments, including the `*args` and `**keywords` argument passing mechanisms.
#
# It is the purpose of the `Args` class to describe these details. Bear in mind that each instance of `Args` will eventually result in one function call.

# %% [markdown]
# You simply build one `Args` instance with the arguments you want to see passed to the function. This supports named arguments as well, and so
#
#     Args(1, 2)
#
# will result in the functions (either student- or teacher-provided) being called like this
#  
#     foo(1, 2)
#     
# and of course similarly 
#
#     Args(1, 2, 3, z=4)
#     
# will trigger
#
#     foo(1, 2, 3, z=4)

# %%
## Variable number of args

# %%
from nbautoeval.exercise_function import ExerciseFunction
from nbautoeval.args import Args 


# %% [markdown]
# If your function accepts a variable number of arguments, it does not matter that much&nbsp;:

# %%
def foo3(a, b, c=10):
    return f"a={a} b={b} c={c}"

foo3_inputs = [
    Args(1, 2, 3),
    Args(4, 5),
]

exo_foo3 = ExerciseFunction(foo3, foo3_inputs, nb_examples=0)

exo_foo3.example()


# %% [markdown]
# ### Named args

# %% [markdown]
# Nothing changes if now the function to be written can handle named arguments. Let's see this on an example&nbsp;:

# %%
def anyfun(a, b, *args, **keywords):
    # always show 2 mandatory args first
    result = f"a={a}, b={b}"
    # if more un-named args are passed
    for i, arg in enumerate(args):
        result += f" + u{i+3}->{arg}"
    for k, v in keywords.items():
        result += f" & {k} -> {v}"
    return result


# %%
# let's first grasp what this function does
anyfun(1, 2, 3, 4, foo='foo')

# %% [markdown]
# Now we can define an exercise that calls this function 3 times with a variety of argument sets

# %%
anyfun_inputs = [
    Args(1, 2, tutu='tutu'),
]

exo_anyfun = ExerciseFunction(anyfun, anyfun_inputs, nb_examples=0)

exo_anyfun.example()

# %% [markdown]
# ## Example

# %% [markdown]
# Students are requested to write a function 
#
# $ curve (a, b, c) \Longrightarrow a^2 + 3ab + c $
#
# with $c$ defaulting to 12.

# %%
from exercises.curve import exo_curve

# %%
exo_curve.example(2)


# %%
# write your solution here
def curve (a, b, c=12):
    return "<...>"


# %% [markdown]
# Imagine she comes up with this - broken on purpose - solution&nbsp;:

# %%
# the student's - broken - proposal
def curve (a, b, c=12):
    return a ** 2 + 3 * a * b + 12 if (a+b)%4 != 0 else False


# %%
exo_curve.correction(curve)

# %% [markdown]
# ## Corresponding python code

# %%
# %cat ../exercises/curve.py
