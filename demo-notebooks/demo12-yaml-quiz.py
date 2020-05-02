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
# # writing a quiz in YAML

# %%
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% [markdown]
# ## YAML

# %% [markdown]
# examples below mostly carry the same contents as the one from demo notebook #8, but this time the tests are written using YAML  
# clearly this is a much nicer approach  
#
# see this nice video tuto if you have 10' to learn about YAML
# https://www.youtube.com/watch?v=cdLNKUoMc6c

# %% [markdown]
# ## single entry point
#
# `run_yaml_quiz(radical, exoname)`
#
# * **first argument** *radical* refers to the source filename  
#   in our example radical is `"quiz-sample"` and it refers to the source for the quiz, which is searched along a built-in heuristic so as to avoid exposing the source in too conspicuous a way  
#   turns out here the actual file is `../yaml/quiz-sample.yaml`
#
# * **second argument** is the name of a quiz inside the YAML code; in this instance the sample YAML defines 2 quizzes named `quiz1` and `quiz2`

# %% [markdown]
# ## first example : basics, and math

# %%
# this is for testing purposes only, it allows to 'reset' the history
# about this particular exercise
from nbautoeval.storage import storage_clear
storage_clear("yaml-sample-one")

# %% scrolled=false
from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz-sample", "quiz1", # debug=True 
                                      # debug=2 # for even more
             )

# %% [markdown]
# ## example #2 - code

# %% [markdown]
# from the same YAML file (see below for code)

# %%
# ditto - this is for testing purposes only, it allows to 'reset' the history
# about this particular exercise

storage_clear("yaml-sample-two")

# %% scrolled=false
# from the same source file as above, but another quiz

from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz-sample", "quiz2", # debug=True
             )

# %% [markdown]
# ## example #3 - markdown

# %% [markdown]
# from the same YAML file (see below for code)

# %%
# ditto - this is for testing purposes only, it allows to 'reset' the history
# about this particular exercise

storage_clear("yaml-sample-three")

# %% scrolled=false
# from the same source file as above, but another quiz

from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz-sample", "quiz3", # debug=True
             )

# %% [markdown]
# # under the hood

# %% scrolled=false
# that's where the actual source code is in our example
# searches in . .. ../.. HOME
# for files named in radical / radical.yml / radical.yaml
# and in subdirs . ./yaml/ ./.yaml/ ./.quiz/
# you can use dirs named .yaml to be even more stealthy
# !cat ../yaml/quiz-sample.yaml

# %%
