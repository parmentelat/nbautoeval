# -*- coding: utf-8 -*-
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
#   notebookname: NO HEADING 1 found
#   version: '1.0'
# ---

# %% [markdown]
# <span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat&nbsp;<img src="../media/inria-25.png" style="display:inline"></span><br/>

# %% [markdown]
# # Note on the environment

# %% [markdown]
# ## Standalone

# %% [markdown]
# See `runserver.sh` so that this example notebook has its `PYTHONPATH` set up properly in a standalone jupyter run.

# %% [markdown]
# ## Under binder

# %%
# just so that it runs smoothly under binder
import sys
sys.path.append("..")

# %% [markdown]
# # A sample exercise with functions

# %% [markdown]
# Let us start with a simple exercise that involves a basic one-argument function.

# %% [markdown]
# ## Explain the problem

# %%
# you need to evaluate this cell
# for the notebook to work properly
from exercises.percentages import exo_percentages

# %% [markdown]
# You are of course expected to describe in plain text what the exercise is all about. In our case we want the student to write a function that expects a string containing only uppercase letters among `ACGT`, and return a dictionary containing their respective percentages.

# %%
# an example of the expected outcome of your (correct) function
exo_percentages.example()


# %% [markdown]
# ## Tell the student to write their own code

# %% [markdown]
# As a rule of thumb, it is advisable to provide something that is syntaxically correct. This way it won't break complete evaluation of the notebook, which can come in handy when doublecheking.

# %%
# write your own implementation here
def percentages(adn):
#    from collections import Counter
#    c = Counter(adn)
#    l = len(adn)
#    ks = ('A', 'C', 'G', 'T')
#    return dict( [(k, 100*c[k]/l) for k in ks] )
    return "your code"


# %% [markdown]
# ## Auto correction

# %% [markdown]
# At this point you just need to insert a cell like the following, and students just need to evaluate
#  * their code
#  * the correction cell
# as many times as they want until it is all green.

# %%
# validez votre code en évaluant cette cellule
exo_percentages.correction(percentages)

# %% [markdown]
# # Under the hood

# %% [markdown]
# Below is what the python code in `percentages.py` looks like; once comments are trimmed down, this amounts to about a dozen lines&nbsp;:

# %%
# %cat ../exercises/percentages.py
