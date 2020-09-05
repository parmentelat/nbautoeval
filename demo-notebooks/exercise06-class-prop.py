# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   notebookname: NO HEADING 1 found
#   version: '1.0'
# ---

# %% [markdown]
# <span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat&nbsp;<img src="../media/inria-25.png" style="display:inline"></span><br/>

# %% [markdown]
# # class-based exercises - part 2

# %%
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")

# %% [markdown]
# ## a property-based class

# %% [markdown]
# ### assignment

# %% [markdown]
# students are requested to write a `Gauge` class that has a single `x` attribute that must be guaranteed to be **between 0 and 100**; any attempt to set it otherwise should result in the attribute being set to 0 or 100, whichever is closest to the intended value.

# %% [markdown]
# ### workflow

# %% [markdown]
# this is quite similar but we need to write **statements** instead of just expressions
#
# * statements can be specified by creating a `ClassStep` object with the `statement=True` parameter
# * statements are run with `exec()` instead of `eval()`, and so it does not make sense to compare the behaviour of the student's class with the reference class; a following expression should be used to check for compliance

# %%
from exercises.gaugeclass import exo_gauge
exo_gauge.example()


# %%
# this class is broken too
class Gauge:
    
    def __init__(self, x):
        self.x = x
        
    def __repr__(self):
        return f"{self.x}"


# %%
exo_gauge.correction(Gauge)

# %% [markdown]
# ### under the hood

# %%
from listing import listing
listing("../exercises/gaugeclass.py")
