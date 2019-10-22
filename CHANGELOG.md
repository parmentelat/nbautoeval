# 0.6.1 - 2019 Oct 21

* DO NOT USE - broken !
* more illustrative examples of generator-based exercises
* unfinished support to passing generators as arguments

# 0.6.0 - 2019 Oct 21

* new classes ExerciseGenerator and GeneratorArgs to build exercises
  where students are to write generator functions
* demo notebooks are ol=nly exposed in jupytext/python format

# 0.5.2 - 2019 Oct 12

* bugfix in class example display
* bugfix in displaying outputs with <> which is the case for 
  default repr() on objects that don't have their own __repr__()

# 0.5.1 - 2019 Oct 12

* improved class definition: 
  * results of constructor step now checked as well
  * no longer need to call `repr()` explicitly
  * now has support for statements w/ ClassExpression and ClassStatement
  * StepClass now renamed into ClassExpression, which breaks from 0.5.0

# 0.5.0 - 2019 Oct 11

* rewrote class-oriented exercise to extend possibilities
* DO NOT USE THIS VERSION as the API has been changed in 0.5.1

# 0.4.7 - 2019 Oct 7

* properly display type objects when used as arguments

# 0.4.6 - 2019 Jul 31

* add requires in particular for when using in readthedocs
* 0.4.3..5 are broken

# 0.4.2 - 2019 Jul 25

* fix label as it show up on pypi
* expose symbols globally

# 0.4.1 - 2018 Sep 26

* bugfix: in the correction table, cells sometimes were missing the <pre> tag
* was during py3s2 in exo_wc, that has an input with 2 consecutive spaces

# 0.4.0 - 2018 Aug 30

* cosmetic changes in example and correction tables
  * vertical bars to separate the columns
  * so that code cells can now be left-aligned
* ability to tweak font sizes (header and plain) for a given exercise

# 0.3.0 - 2018 Jan 5

* merge changes from flotpython
* including ExerciseFunctionNumpy
* and ExerciseFunction.validate()

# 0.2.0 - 2017 Jul 3

* env. variable NBAUTOEVAL_LOG can set location for the log file
* default is now $HOME/.nbautoeval

# 0.1.3 - 2017 Feb 3

* use find_packages()

# 0.1.2 - 2017 Feb 3

* add a MANIFEST.in

# 0.1.1 - 2017 Feb 3

* first versioned release
* available in pypi
