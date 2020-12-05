# pylint: disable=c0111
import numpy as np

from nbautoeval import Args, ExerciseFunctionNumpy, ImshowRenderer


# @BEG@ name=checkers
def checkers(size):
    """
    Un damier
    le coin (0, 0) vaut 0
    """
    I, J = np.indices((size, size))
    return (I + J) % 2
# @END@


checkers_inputs = [
    Args(3),
    Args(1),
    Args(0),
    Args(2),
    Args(4),
]


exo_checkers = ExerciseFunctionNumpy(
    checkers,
    checkers_inputs,
    nb_examples=2,
    result_renderer=ImshowRenderer(css_width="100px", cmap='gray'),
)
