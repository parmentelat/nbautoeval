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
# # testing math stuff

# %% {"scrolled": true}
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")

# %% [markdown]
# ## matrices

# %% {"hide_input": false, "scrolled": false}
from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz04-math", "quiz-matrices")

# %%
# XXX this is for demo purposes only XXX
# XXX so counters may be reset XXX 

from nbautoeval.storage import storage_clear
storage_clear("matrices-exoname")

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizzes

# %% {"scrolled": false, "cell_style": "center"}
from listing import listing
listing("yaml/quiz04-math.yaml")
