# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import sys
sys.path.append("..")

# %%
from nbautoeval.quiz_loader import YamlLoader, locate_from_radical
from nbautoeval import run_yaml_quiz

# %%
# designed to be run manually in a notebook
# we return both quiz and widget but that is for debugging only

exported = None

def manual_test_colors(debug=False, trim_explanations=False):
    filename = locate_from_radical("test-colors", debug)
    loader = YamlLoader(filename)
    quiz = loader.build_quiz("color-quiz", debug)
    if trim_explanations:
        for question in quiz.questions:
            question.explanation = None
            for option in question.options:
                option.explanation = None
    widget = quiz.widget()

    q1, q2, q3, q4 = quiz.questions
    # first 2 are unanswered, so no clic
    # 3rd one is a right question so we click the 1st option
    q3.checkboxes[0].value = True
    # 4th one is wrong but not un answered, and we want an asortment
    q4.checkboxes[0].value = True
    q4.checkboxes[1].value = True

    return quiz, widget


# %%
from nbautoeval.storage import storage_clear
storage_clear("color-quiz")

# %%
# the sample qui where we manually remove the explanations
q, w = manual_test_colors(trim_explanations=True)
w

# %% scrolled=false
# with explanations
q, w = manual_test_colors()
w
