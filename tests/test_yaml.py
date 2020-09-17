from pathlib import Path

import pytest

from ipywidgets import Widget

from nbautoeval.quiz_loader import YamlLoader, run_yaml_quiz

localdir = Path(__file__).parent
yamldir = localdir.parent / "tests"

def test_rain_check():
    for file in yamldir.glob("test-ko-*.yaml"):
        with pytest.raises((ValueError, AssertionError)):
            YamlLoader(file).rain_check()

def test_exoname1():
    witness = "quiz1"
    loader = YamlLoader(yamldir / "test-ok-1.yaml")
    quiz = loader.build_quiz(witness, True)
    assert quiz.exoname == witness

def test_exoname2():
    witness = "quiz1"
    loader = YamlLoader(yamldir / "test-ok-2.yamlb")
    quiz = loader.build_quiz(witness, True)
    assert quiz.exoname == witness

# black box testing
def test_all_in_one():
    w1 = run_yaml_quiz("test-ok-1", "quiz1")
    assert isinstance(w1, Widget)
    w2 = run_yaml_quiz("test-ok-2", "quiz1")
    assert isinstance(w2, Widget)
