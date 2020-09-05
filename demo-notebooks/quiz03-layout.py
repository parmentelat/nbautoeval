# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed
#     cell_metadata_json: true
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # layout in quizzes

# %% {"scrolled": true}
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")

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
# XXX this is for demo purposes only XXX
# XXX so counters may be reset XXX 

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
# XXX this is for demo purposes only XXX
# XXX so counters may be reset XXX 

from nbautoeval.storage import storage_clear
storage_clear("demo-layout-exoname")

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizzes

# %% {"scrolled": false, "cell_style": "center"}
from listing import listing
listing("yaml/quiz03-layout.yaml")
