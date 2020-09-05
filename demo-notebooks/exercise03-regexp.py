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
#   notebookname: A sample regular expression exercise
#   version: '1.0'
# ---

# %% [markdown]
# <span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat&nbsp;<img src="../media/inria-25.png" style="display:inline"></span><br/>

# %%
# optional and specific to our use case
# see first demo notebook for an explanation about this cell
import sys
sys.path.append("..")

# %% [markdown]
# # A sample regular expression exercise

# %%
from exercises.regexp import exo_at_least_two

# %% [markdown]
# Same workflow, but this time the student is asked to write a REGEXP. In this case we want them to write a regexp that will find at least 2 successive occurences of `TA`.

# %%
exo_at_least_two.example()

# %% [markdown]
# At that point you will like always offer a cell for the students to give their own solution
#

# %%
# do not call re functions, just define the pattern
at_least_two = "<your pattern>"

# %% [markdown]
# And a cell for checking it against the correct implementation&nbsp;:

# %%
exo_at_least_two.correction(at_least_two)

# %% [markdown]
# # Under the hood

# %% [markdown]
# Here's the python code for this exercise

# %%
from listing import listing
listing("../exercises/regexp.py")

# %% [markdown]
# # Other variants

# %% [markdown]
# ## `ExerciseRegexp` class, with other policies

# %% [markdown]
# This exercise uses the `finditer` matching policy. As you can see, with this policy, what gets displayed is a list of tuples `(begin, end)` with the indices of where the pattern is found. 

# %% [markdown]
# The following policies are supported as well, depending on which function in the `re` module actually gets called - feedback is appreciated as this currently is far from perfect&nbsp;:
#
# * `match` : the regular expression is searched at the beginning of the string only, with `re.match`
# * `find` : likewise with `re.find`
# * `findall` : uses `re.findall`

# %% [markdown]
# ## `ExerciseRegexpGroups` class

# %% [markdown]
# This class will work better with patterns that define named groups, and attemps to leverage that for improving rendering of the results.

# %% [markdown]
# ## Known issues

# %% [markdown]
# Not all 8 combinations (2 classes, 4 policies) have been very thoroughly tested so far.

# %% [markdown]
# *****
# *****
# *****
# *****

# %% [markdown]
# # Tip for troubleshooting

# %% [markdown]
# It can be tedious to close and re-open a notebook each time that a change is made. A few options in these situations&nbsp;:
#
#
# * use autoreload
#   * either explicitly in (at the top of) your notebook 
#     ```
#     %load_ext autoreload
#     %autoreload 2
#     ```
#   * or automatically by tweaking your ipython profile
#     ```
#     $ cat ~/.ipython/profile_default/ipython_config.py
#     c.InteractiveShellApp.exec_lines = []
#     c.InteractiveShellApp.exec_lines.append('%load_ext autoreload')
#     c.InteractiveShellApp.exec_lines.append('%autoreload 2')
#     ```
# * In my environment I have a keyboard shortcut to restart the kernel - no questions asked.
# * You can also do it in native python itself (here for python3), but you need to recall to clean it up, it is not recommended

# %%
import exercises
import importlib
importlib.reload(exercises.regexp)
