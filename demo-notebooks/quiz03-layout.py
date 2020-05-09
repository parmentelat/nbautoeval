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
# # layout in quizzes

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% [markdown]
# ## shuffling and randomizing

# %% [markdown]
# About **shuffling** of contents :
#
# * shuffling options within a question is a fairly straightforward feature and is the default in our model;
# * shuffling questions within a quiz is rather standard as well, and is the default as well
# * in both cases, this can be turned off by setting `shuffle=False` on the related `QuizQuestion` or `Quiz` object, respectively;
#
# Randimizing contents, OTOH, is **currently not supported**; all students will get the same set of questions and options, just in a different order. The effort required to get this right, in particular wrt storing results between 2 attempts, was deemed excessive at his point.
# One other thing that looked overly complex is that, in our model, a quiz is a flat list of questions, and there is no additional structure there, so e.g. if you want to say 'pick 4 questions among these 6, and then 3 among these 5' it would require 2 separate `Quiz` instances just to materialize this grouping. 

# %% {"hide_input": false, "scrolled": false}
from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz03-layout", "quiz-demo-shuffle")

# %%
# XXX this is for testing purposes only XXX
from nbautoeval.storage import storage_clear
storage_clear("demo-shuffle-exoname")

# %% [markdown]
# ## layout

# %% [markdown]
# The default is a totally vertical layout, let's see the effect of 2 attributes that can be set on a `QuizQuestion` instance to tweak that default layout

# %% {"hide_input": false, "scrolled": false}
from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz03-layout", "quiz-demo-layout")

# %%
# XXX this is for testing purposes only XXX
from nbautoeval.storage import storage_clear
storage_clear("demo-layout-exoname")

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizzes

# %% {"scrolled": false, "cell_style": "center"}
# !cat yaml/quiz03-layout.yaml
