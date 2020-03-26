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
# # some quizzes 

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% {"scrolled": true}
# for convenience in development
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## a quizz is made of questions

# %% [markdown]
# a Quiz object contains one or several questions; here is an example with a single question

# %% {"scrolled": false}
from exercises.quizsample import single_quiz
single_quiz.widget()

# %% [markdown]
# ## more questions
#
# in this notebook the correct answers are always the one starting with 'a'

# %% {"hide_input": false, "scrolled": false}
from exercises.quizsample import quiz
quiz.widget()

# %% [markdown]
# ## under the hood

# %% {"scrolled": true}
# !cat ../exercises/quizsample.py
