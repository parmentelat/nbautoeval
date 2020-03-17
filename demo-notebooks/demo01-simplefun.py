# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   notebookname: NO HEADING 1 found
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: false
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: false
#   version: '1.0'
# ---

# %% [markdown]
# <span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat&nbsp;<img src="../media/inria-25.png" style="display:inline"></span><br/>

# %% [markdown]
# # Note on the environment

# %% [markdown]
# ## For binder

# %% [markdown]
# So that Python can find the `nbautoeval` package, especially under binder:

# %%
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
    # this code is providing one of the correct answers
    # to illustrate the rendering
    return {'A': 37.5,
            'C': 25.0,
            'G': 25.0,
            'T': 12.5}


# %% [markdown]
# ## Auto correction

# %% [markdown]
# At this point you just need to insert a cell like the following, and students just need to evaluate
#  * their code
#  * the correction cell
# as many times as they want until it is all green.
#
# of course if you'd prefer you can merge both cells so students only need to evaluate one cell; the risk however with that mode is when beginners get lost they can also lose the correction code if it is in the same cell as their own code...

# %%
# validez votre code en évaluant cette cellule
exo_percentages.correction(percentages)

# %% [markdown]
# # Under the hood

# %% [markdown]
# Below is what the python code in `percentages.py` looks like; once comments are trimmed down, this amounts to about a dozen lines&nbsp;:

# %%
# %cat ../exercises/percentages.py
