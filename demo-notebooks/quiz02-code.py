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
# # dealing with code in quizzes

# %% {"scrolled": true}
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")

# %% [markdown]
# The YAML format allows to specify an optional `text`; for example
#
# ```
#   question: |
#     the body of a
#     multi-line question
# ```
#
# is a shorthand for actually this :
#
# ```
#   question: 
#     text: |
#       the body of a
#       multi-line question
# ```
#
# the second form is typically required when more details must be set; so typical idioms include
#
# ```
#   options:
# # simplest
#     - "a single-line option"
# # but if it's a correct one you need to write
#     - text: "a single-line option"
#       correct: true
# # and if you want to specify an alternative type
#     - text: "a single-line option"
#       type: CodeOption
#       correct: true
# ```

# %% [markdown]
# ## examples of code in questions and options

# %% {"hide_input": false, "scrolled": false}
from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz02-code", "quiz-demo-code")

# %%
# XXX this is for testing purposes only XXX
from nbautoeval.storage import storage_clear
storage_clear("demo-code-exoname")

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizzes

# %% {"scrolled": false, "cell_style": "center"}
from listing import listing
listing("yaml/quiz02-code.yaml")
