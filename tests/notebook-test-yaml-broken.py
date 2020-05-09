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
# # broken quizzes

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% [markdown]
# ## sanity checks

# %% [markdown]
# Here's a few examples of broken definitions, and how they are notified to the teacher; note that this sanity check happens upon creation of the Quiz instance, no need to call widget() to be notified

# %%
from nbautoeval import run_yaml_quiz

run_yaml_quiz("test-broken", "quiz-broken")

# %% [markdown]
# Also note that there's no runtime outlining of a broken quiz, for now at least... 

# %%
# this is for testing purposes only, it allows to 'reset' the history
# about this particular exercise
from nbautoeval.storage import storage_clear
storage_clear("quiz-broken")

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizz

# %% {"scrolled": false}
# !cat ./test-broken.yaml
