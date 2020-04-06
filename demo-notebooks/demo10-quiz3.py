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
# # mimicking an older quiz

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% {"scrolled": true}
# for convenience in development
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# Starting from a sample quiz provided by C. Joly, we demonstrate a couple features and show how that initial sample could be approximated within the nbautoeval model.
#
# About shuffling and randomizing : see also [./demo09-quiz2.py](this other demo notebook] for more examples about this.

# %% [markdown]
# ## the quiz

# %%
# this is for testing purposes only, it allows to 'reset' the history
# about this particular exercise
from nbautoeval.storage import storage_clear
storage_clear("quiz-sample-mines")

# %% {"scrolled": false}
from exercises.quiz_mines import quiz
quiz.widget()

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizz

# %% {"scrolled": false}
# !cat ../exercises/quiz_mines.py
