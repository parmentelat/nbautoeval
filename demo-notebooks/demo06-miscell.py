# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
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
#   notebookname: Not limited to functions
#   version: '1.0'
# ---

# %% [markdown]
# <span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat&nbsp;<img src="../media/inria-25.png" style="display:inline"></span><br/>

# %%
# just so that it runs smoothly under binder
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
# In such a case, the frameork needs to copy the input data, otherwise the student- and teacher-provided functions would not operate on comparable inputs.
#
# This is the purpose of the `copy_mode` flag, which by default is 'deep' which means deep copy, it is sometimes useful to use other methods.
#

# %% [markdown]
# # Tweaking the way things are displayed

# %% [markdown]
# This is an area where a lot of trials and errors did take place. Not sure that it's right in any way in the current status. In any case check out the arguments that the Exercise constructors know about. Among them&nbsp;:
#
# * You can specify in `layout_args` a layout for the 3 columns, specified in character widths.
# * `layout` defaults to `pprint`, other policies are available as well, you'll need to check in the code
# * same for `call_layout` which
# * `render_name` can be set to False to save space in the leftmost column (see example below)
# * `nb_examples` says how may examples should be shown (datasets used in order from index 0, of course). This can be superseded in the call to `example` too
#

# %% [markdown]
# ##### Example with and without `render_name`

# %% [markdown]
# Defining an `ExerciseFunction` with `render_name=False` will cause a slightly different output, in an attempt to save space.

# %%
def curve(a, b, c=12): 
    # make it work only when a==b
    return a ** 2 + 3 * a * b + c + (a - b)



# %%
# the default is to display the function name in 1st column
from exercises.curve import exo_curve
exo_curve.correction(curve)

# %%
# this Exercise instance has render_name = False
from exercises.curve import exo_curve_noname
exo_curve_noname.correction(curve)
