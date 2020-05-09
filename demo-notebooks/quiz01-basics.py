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
# # one sample quiz 

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% [markdown]
# ## quizzes in YAML files

# %% [markdown]
# A quiz object is a collections of questions; each question has several options, at least one of which being correct.
#
# You can define a quiz inside a YAML file; we'll see a few simple examples below (it is possible to define quizzes in Python as well, but not recommended for getting started.
#
# One YAML file can define several quizzes.

# %% [markdown]
# ## quiz basics : contents, logic and scores
#
# in this notebook the correct answers are always the one starting with 'a' or $\alpha$

# %% {"hide_input": false, "scrolled": false}
from nbautoeval import run_yaml_quiz

# first argument:
#    the stem for the (yaml) filename, 
# second argument:
#    the name of the quiz defined in the YAML content
run_yaml_quiz("quiz01-basics", "quiz-basics")

# %%
# XXX this is for testing purposes only XXX
# it allows to 'reset' the history about this particular exercise
# if you reach the maximum number of attemps and want to start again
from nbautoeval.storage import storage_clear

# to do that one needs to know the 'exoname' attached 
# to that quiz
storage_clear("quiz-content-my-exoname")

# %% [markdown]
# ## Quiz epilogue, and explanations

# %% [markdown]
# When the student has it all right, or when `max_attempts` is reached (that is a Quiz attribute), the student can see their result; options that were not properly ticked or unticked are outlined in red; additional hints - code keyword is `explanation` are also unveiled if present.

# %%
run_yaml_quiz("quiz01-basics", "quiz-explanations")

# %%
# XXX this is for testing purposes only XXX
# it allows to 'reset' the history about this particular exercise
# if you reach the maximum number of attemps and want to start again
from nbautoeval.storage import storage_clear

# to do that one needs to know the 'exoname' attached 
# to that quiz
storage_clear("explanations")

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizzes

# %% {"scrolled": false, "cell_style": "center"}
# !cat yaml/quiz01-basics.yaml

# %%
