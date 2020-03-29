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

# %% {"scrolled": true}
# for convenience in development
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## a quiz is made of questions
#
# in this notebook the correct answers are always the one starting with 'a'

# %% {"hide_input": false, "scrolled": false}
from exercises.quizsample import quiz1, quiz2
quiz1.widget()

# %%
quiz2.widget()

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizz

# %% {"scrolled": false}
# !cat ../exercises/quizsample.py
