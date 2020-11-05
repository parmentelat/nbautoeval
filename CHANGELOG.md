# 1.6.3 - 2020 Nov 5

* improved nbae-quiz-scan script

# 1.6.2 - 2020 Nov 3

* slight cosmetic tweak in class scenarios rendering
* 1.6.1 is broken

# 1.6.0 - 2020 Oct 30

* new `ImshowRenderer` for numpy arrays
* close #25
* close #28

# 1.5.3 - 2020 Oct 19

* minor cosmetic tweaks

# 1.5.2 - 2020 Sep 15

* feedback on submit shows results for past attempts

# 1.5.1 - 2020 Sep 12

* cosmetic change in quiz_help()

# 1.5.0 - 2020 Sep 4

* changed to use markdown-it-py directly, with a lighter dependency footprint
* new function quiz_help() in english and french

# 1.4.0 - 2020 Sep 4

* fix for using myst-parser 0.12

# 1.3.0 - 2020 Aug 28

* implement #22 - questions with multiple exactly_one_option = False
  are by default using progressive grading
* plus cosmetic changes in rendering the score of each question
* each attempt displays the corresponding score

# 1.2.0 - 2020 Aug 14

* support for base64-encoded yaml quiz

# 1.1.6 - 2020 Jun 3

* drop userid altogether, this is fragile and not meningful anyway, 
  it is not even exposed in the new json format

# 1.1.5 - 2020 Jun 3

* for Windows, replace os.getuid() with os.getlogin()
* cosmetic tweaks in demo notebooks, including pure Python listing() helper
  to display files on Windows

# 1.1.4 - 2020 May 18

* groupes vs groups
* grade-quiz.py based on json and .nbautoeval.trace

# 1.1.3 - 2020 May 12

* based on shareable Makefile.pypi

# 1.1.2 - 2020 May 12

* Makefile now uses twine for publishing onto pypi 
* no change in the library itself
* slight brushes in the doc


# 1.1.1 - 2020 May 8

* fixed awkward bug in rendering contents  
  the MarkdownMathContent and MarkdownMathOption classes
  should now fit most common needs, and are the new defaults
* expose class `MathContent` for consistency
* documentation on quizzes rewritten to focus on YAML, 
  has become much cleaner and shorter

# 1.1.0 - 2020 May 4

* teachers can define their quiz in yaml
  and display them with run_yaml_quiz()
* quiz questions and options objects can have an explanation 
  that gets revealed when the quiz is finished (#12)
* improved traces kept when students validate their work
* new class CodeContent exposed for consistency
* rough tool for grading quizzes
* new dependency to PyYAML
* markdown engine replacement for issue #16  
  MyST a.k.a. myst_parser replaces markdown2

# 1.0.1 - 2020 Apr 23

* cosmetic tweaks

# 1.0.0 - 2020 Apr 7

* this version is ***not backward-compatible** with 0.6 and below
* rendering engine entirely rewritten to take advantage of ipywidgets
* as a consequence all 4 flavours of `Exercise` have a different 
  interface for tweaking how results are being shown up;  
  as an example, `ExerciseFunction` accepts a `call_renderer` 
  and a `result_renderer` attribute, that decide how to format
  the call column (1st) and result columns (2nd and 3rd)
* new Quiz feature to define multiple-choice tests

# 0.6.5 - 2020 Mar 24

* no new feature, just a minor cleanup before big rewrite

# 0.6.4 - 2019 Dec 10

* feature for issue #9: an ExerciseClass instance can be created with check_init=False

# 0.6.3 - 2019 Nov 25

* bugfix for issue #7

# 0.6.2 - 2019 Oct 24

* essentially same features as 0.6.0, except for `copy_mode="tee"` 
  that remains an available option but only explicitly
  as it breaks some of our gen-based exos

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
