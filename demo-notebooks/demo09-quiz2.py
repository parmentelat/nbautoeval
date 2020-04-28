# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     cell_metadata_json: true
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
# ---

# %% [markdown]
# # other quiz examples

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% [markdown]
# ## shuffling and randomizing

# %% [markdown]
# about shuffling and randomizing of contents :
#
# * shuffling options within a question is a fairly straightforward feature and is the default in our model;
# * shuffling questions within a quiz is rather standard as well; it is not the default at this point, 
#   but can easily be turned on when creating a `Quiz` instance with `shuffle=True`
# * randomizing questions within a quiz is available as well as an experimental feature; for now you would need to define the number of questions to ask with random_questions=<n>
#
# one thing that is maybe **not optimal yet** is that in our model a quiz is a flat list of questions, there is no additional structure there, so e.g. if you want to say 'pick 4 questions among these 6, and then 3 among these 5' it is going to require 2 separate `Quiz` instances just to materialize this grouping
#

# %%
# this is for testing purposes only, it allows to 'reset' the history
# about this particular exercise
from nbautoeval.storage import storage_clear
storage_clear("quiz-sample-extras")

# %%
from exercises.quiz_extras import quiz_extras
quiz_extras.widget()

# %% [markdown]
# ### under the hood

# %% {"scrolled": false}
# !cat ../exercises/quiz_extras.py

# %% [markdown]
# ## quiz layout options

# %% [markdown]
# here are a few examples that demonstrate the basics

# %%
# this is for testing purposes only, it allows to 'reset' the history
# about this particular exercise
from nbautoeval.storage import storage_clear
storage_clear("quiz-sample-layout")

# %% {"scrolled": false}
from exercises.quiz_layout import quiz_layout
quiz_layout.widget()

# %% [markdown]
# ### under the hood

# %% [markdown]
# Here's the code that defines the above quizz

# %% {"scrolled": false}
# !cat ../exercises/quiz_layout.py
