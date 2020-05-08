from pathlib import Path

import pytest

from ipywidgets import Widget

from nbautoeval.quiz_loader import YamlLoader, run_yaml_quiz

localdir = Path(__file__).parent
yamldir = localdir.parent / "yaml"

def test_rain_check():
    for file in yamldir.glob("qko*.yaml"):
        with pytest.raises((ValueError, AssertionError)):
            YamlLoader(file).rain_check()
            
def test_exoname1():
    witness = "quiz1"
    loader = YamlLoader(yamldir / "qok1.yaml")
    quiz = loader.build_quiz(witness, True)
    assert quiz.exoname == witness

# black box testing
def test_all_in_one():
    w = run_yaml_quiz("qok1", "quiz1")
    assert isinstance(w, Widget)
