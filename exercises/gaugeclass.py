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
    
    def __repr__(self):
        return f"{self._x}"


# create an exercise instance

from nbautoeval.exercise_class import (
    ExerciseClass, ClassScenario, ClassExpression, ClassStatement)
from nbautoeval.args import Args

scenario1 = ClassScenario(
    # arguments to the constructor
    Args(10),
    # statements need to be tagged as such 
    ClassStatement("INSTANCE.x = 50"),
    ClassStatement("INSTANCE.x = 2000"),
)

scenario2 = ClassScenario(
    # arguments to the constructor
    Args(1000),
    # note that a str object passed here is actually
    # used to create a ClassExpression object
    ClassStatement("INSTANCE.x = -1000"),
)


exo_gauge = ExerciseClass(
    Gauge, [scenario1, scenario2],
    obj_name = "gauge",
    )

if __name__ == '__main__':
    exo_gauge.example()
    exo_gauge.correction(Gauge)

