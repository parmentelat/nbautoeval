# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.7
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
# # class-based exercises

# %%
# %load_ext autoreload
# %autoreload 2

# %%
# just so that it runs smoothly under binder
import sys
sys.path.append("..")

# %% [markdown]
# ## intro

# %% [markdown]
# creating a class-based exercise currently means:
#
# * writing a reference class
# * defining a suite of *Scenarios*
#
# each Scenario in turn means
# * creating one witness instance, from one `Args` object
# * run several expressions and/or statements in a context where
#   * `INSTANCE` is replaced with the witness object, and
#   * `CLASS` is replaced with the class object under test

# %% [markdown]
# *****

# %% [markdown]
# ## comparing objects

# %% [markdown]
# ### using `repr()` in constructor and statements
#
# for the first step of a class scenario (calling the constructor), as well as for statement steps, the actual result that we get from code evaluation is `None`.  
# so in these case, in order to check for correctness we **compare both objects `repr()`s**

# %% [markdown]
# ### using `repr()` when expression returns an object
#
# similarly, when the scenario expression returns an object (think of the addition of two objects), we cannot compare results using `==` because the two objects (one under reference implementation and one under student implementation) are of different classes and thus would not be considered equal by `==`
#
# so in these situations again, the two objects are compared through their `repr()` textual representation.

# %% [markdown]
# ### bottom line
#
# this all means that students need to pay extra attention to have their `__repr__()` method work exactly as requested, otherwise they get a lot of false negative.

# %% [markdown]
# *****

# %% [markdown]
# ## a FIFO

# %% [markdown]
# This section demonstrates how to run a simple (expressions-only) class scenario.
# Next section introduces the notion of statements-oriented scenariis, useful typically to deal with properties.

# %% [markdown]
# ### Assignment

# %% [markdown]
# Students are requested to write a `Fifo` class, that implements
# * a constructor `Fifo()`
# * an `incoming(obj)` method
# * an `outgoing()` method
#
# that just returns the elements in the same order as they were stored.

# %% [markdown]
# ### Workflow

# %%
from exercises.fifoclass import exo_fifo
exo_fifo.example()


# %% [markdown]
# Students are then invited to write their code in a cell that initially could look like this&nbsp;:

# %%
# write your code in this cell
class Fifo:
    def __init__(self):
        pass
    def __len__(self):
        pass
    def incoming(self, obj):
        pass
    def outgoing(self):
        pass


# %% [markdown]
# Then she changes it, let's imagine the outcome is this attempt - which is broken on purpose&nbsp;:

# %%
# code is BROKEN ON PURPOSE

# write your code in this cell
class Fifo:
    def __init__(self):
        self.items = []
    def incoming(self, obj):
        self.items.append(obj)
    def outgoing(self):
        if len(self.items)%2 == 0:
            raise Exception(f"even length ->{self.items.pop()}")
        return self.items.pop()


# %% [markdown]
# Then she can evaluate this correction cell

# %%
exo_fifo.correction(Fifo)

# %% [markdown]
# *********

# %% [markdown]
# ### Under the hood

# %% [markdown]
# as always, the python code here can be seen below:

# %%
# %cat ../exercises/fifoclass.py

# %% [markdown]
# *****

# %% [markdown]
# ## a property-based class

# %% [markdown]
# ### assignment

# %% [markdown]
# students are requested to write a `Gauge` class that has a single `x` attribute that is guaranteed to be **between 0 and 100**; any attempt to set it otherwise should result in the attribute being set to 0 or 100, whichever is closest to the intended value.

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
# !cat ../exercises/gaugeclass.py
