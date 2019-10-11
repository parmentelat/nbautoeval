# -*- coding: utf-8 -*-
# 
# a very small class with a property
# 

MIN = 0
MAX = 100

class Gauge:
    
    def __init__(self, x):
        self.x = x
        
    def _get_x(self):
        return self._x
    
    def _set_x(self, x):
        self._x = min(MAX, max(MIN, x))
        
    x = property(_get_x, _set_x)


# create an exercise instance

from nbautoeval.exercise_class import ExerciseClass, ClassScenario, ClassStep
from nbautoeval.args import Args

scenario1 = ClassScenario(
    # arguments to the constructor
    Args(10),
    # a list of expressions, with 
    # INSTANCE and CLASS replaced as appropriate
    "INSTANCE.x",
    ClassStep("INSTANCE.x = 50", statement=True),
    "INSTANCE.x",
    ClassStep("INSTANCE.x = 2000", statement=True),
    "INSTANCE.x",
)

scenario2 = ClassScenario(
    # arguments to the constructor
    Args(1000),
    # a list of expressions, with 
    # INSTANCE and CLASS replaced as appropriate
    "INSTANCE.x",
    ClassStep("INSTANCE.x = -1000", statement=True),
    "INSTANCE.x",
)


exo_gauge = ExerciseClass(
    Gauge, [scenario1, scenario2],
    obj_name = "gauge",
    )

if __name__ == '__main__':
    exo_gauge.example()
    exo_gauge.correction(Gauge)

