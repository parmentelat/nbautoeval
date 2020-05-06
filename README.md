# `nbautoeval`

`nbautoeval` is a very lightweight python framework for creating **auto-evaluated**
exercises inside a jupyter (python) notebook.

two flavours of exercises are supported at this point :

* code-oriented : given a text that describes the expectations, students are invited to
  write their own code, and can then see the outcome on teacher-defined data samples,
  compared with the results obtained through a teacher-provided solution, with a visual
  (green/red) feedback
* quizzes : a separate module allows to create quizzes

At this point, due to lack of knowledge/documentation about open/edx (read: the
version running at FUN), there is no available code for exporting the results as
grades or anything similar (hence the `autoeval` name).

There indeed are provisions in the code to accumulate statistics on all
attempted corrections, as an attempt to provide feedback to teachers.

# Try it on `mybinder`

Click the badge below to see a few sample demos under `mybinder.org` - it's all
in the `demo-notebooks` subdir.

**NOTE** the demo notebooks ship under a `.py` format and require `jupytext` to be
installed before you can open them in Jupyter.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/parmentelat/nbautoeval/master?filepath=demo-notebooks)


# History

This was initially embedded into a [MOOC on
python2](https://github.com/parmentelat/flotpython) that ran for the first time on [the
French FUN platform](https://www.france-universite-numerique-mooc.fr/) in Fall 2014. It
was then duplicated into a [MOOC on
bioinformatics](https://github.com/parmentelat/flotbioinfo) in Spring 2016 where it was
named `nbautoeval` for the first time, but still embedded in a greater git module.

The current git repo is created in June 2016 from that basis, with the intention
to be used as a git subtree from these 2 repos, and possibly others since a few
people have proved interested.

# Installation

```
pip install nbautoeval
```

# Overview

## code-oriented

Currently supports the following types of exercises
  * `ExerciseFunction` : the student is asked to write a function
  * `ExerciseRegexp` : the student is asked to write a regular expression
  * `ExerciseGenerator` : the student is asked to write a generator function 
  * `ExerciseClass` : tests will happen on a class implementation

A teacher who wishes to implement an exercise needs to write 2 parts :

* One python file that defines an instance of an exercise class; this in a nutshell
  typically involves
  * providing one solution (let's say a function) written in Python
  * providing a set of input data
  * plus optionnally various tweaks for rendering results

* One notebook that imports this exercise object, and can then take advantage of it to
  write jupyter cells that typically
  * invoke `example()` on  the  exercise  object to show examples of the expected output
  * invite the student to write their own code
  * invoke `correction()` on  the  exercise  object to display the outcome.

## quizzes

Here again there will be 2 parts at work :

* The recommended way is to define quizzes in YAML format :
  * one YAML file can contain several quizzes - see examples in the `yaml/` subdir
  * and each quiz contain a set of questions
  * grouping questions into quizzes essentially makes sense wrt the maximal number of
    attempts
  * mostly all the pieces can be written in markdown (currently we use `myst_parser`)

* then one invokes `run_yaml_quiz()` from a notebook to display the test
  * this function takes 2 arguments, one to help locate the YAML file
  * one to spot the quiz inside the YAML file
  * run with `debug=True` to pinpoint errors in the source
  
## results and storage

Regardless of their type all tests have an `exoname` that is used to store information
about that specific test; for quizzes it is recommended to use a different name than 
the quiz name used in `run_yaml_quiz()` so that students cant guess it too easily.

stuff is stored in 2 separate locations :

* `~/.nbautoeval.trace` contain one JSON line per attempt (correction or submit)
* `~/.nbautoeval.storage` for quizzes only, preserves previous choices, number of attempts

# Known issues

see https://github.com/parmentelat/nbautoeval/issues
