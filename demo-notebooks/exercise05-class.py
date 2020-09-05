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
# # class-based exercises

# %%
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")

# %% [markdown]
# ## intro: scenario, expressions vs statements

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
# Each part of a scenario is explicitly tagged as either expression or statement; for example :
#
# ```python
# scenario1 = ClassScenario(
#     # arguments to the constructor
#     Args(),
#     # a list of expressions, with 
#     # INSTANCE and CLASS replaced as appropriate
#     ClassExpression("INSTANCE.incoming(1)"),
#     ClassStatement("INSTANCE.incoming(1)"),
# )
# ```

# %% [markdown]
# ***What does that mean*** and how to choose between both ?  
#
# Well quite simply, with this example what would happen would be :
# * in a first step (corresponding to the `Args()` line), the scenario creates an instance by calling the class with no argument
# * in a second step we send the `incoming()` method on that object; because it is tagged as a **`ClassExpression`**, it is the **result of that method** that is used to compare the official solution with the student's code
# * on the other hand in the last step, we send the same method, but because this is tagged as a **`ClassStatement`**, we will **ignore any result** (technically btw, using `exec` instead of `eval`, allowing for a wider spectrum of constructions), and instead **compare the object's status** after the statement.
#
# hopefully we will see more meaningful examples below..

# %% [markdown]
# ## a FIFO for newbies

# %% [markdown]
# we start by demonstrating how to write an assignement for total newbies, who have never heard about how to customize `repr()`. 
#
# Let us demonstrate this with a `ExerciseClass` instance that
#
# * is created with `check_init=False`, meaning the object's internal status is not checked after the constructor gets called, and
# * its scenarios do not involve any statement, because in that case again we'd need the students to write a proper `__repr__()`

# %%
from exercises.fifoclass import exo_fifo_newbies

exo_fifo_newbies.example()


# %% [markdown]
# And in order to validate this assignement it is enough to write this

# %%
class FifoNewbie:

    def __init__(self):
        self.items = []
        
    def incoming(self, incoming):
        self.items.append(incoming)

    def outgoing(self):
        return None if not self.items else self.items.pop(0)


# %%
# this should be all green
exo_fifo_newbies.correction(FifoNewbie)

# %% [markdown]
# ## a more advanced/realistic FIFO

# %% [markdown]
# as soon as the students have learned to write a `__repr__()`, the above limitations no longer hold; let us see an example with the same old Fifo example :

# %%
# now we can ask for more careful implementations
# here we ask for len(), and also for repr()!

from exercises.fifoclass import exo_fifo
exo_fifo.example()

# %% [markdown]
# Note that the above rustic implementation would not fit; not only because we had defined `__len__()`, but more centrally due to the absence of `__repr__()`; let us see how this first implementation would evaluate now

# %%
# the rustic version without __repr__ has no chance to pass
# not even the firs step !

exo_fifo.correction(FifoNewbie)

# %% [markdown]
# ## more notes on `repr()`

# %% [markdown]
# at the risk of repeating some of the material above :

# %% [markdown]
# ### why do we use `repr()` ? 
#
# Consider the case of an expression that returns an object (think e.g. about the addition of two objects).
# We cannot compare results using `==`, because the two objects (one under reference implementation and one under student implementation) are **of different classes** and thus would not be considered equal by `==`

# %% [markdown]
# ### when do we use `repr()` ? 
#
# * in constructor and statements, because that does not return anything, so the only thing we can check is the subject object
# * and, as mentioned above, in expressions that return an object.
#
# So in these cases, in order to check for correctness we **can only compare both objects `repr()`s**

# %% [markdown]
# ### get your `repr()` right
#
# This all means that students need to pay extra attention to have their `__repr__()` method work exactly as requested, otherwise they get a lot of false negative.
#
# if that's too big of a problem (a convoluted repr()) you can always provide the code yourself, although I have found this idea to be sometimes too intrusive, as it tends to suggest my implementation.
#
#

# %% [markdown]
# *********

# %% [markdown]
# ### Under the hood

# %% [markdown]
# as always, the python code here can be seen below:

# %% hide_input=false
from listing import listing
listing("../exercises/fifoclass.py")
