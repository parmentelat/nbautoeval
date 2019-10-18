from nbautoeval import ExerciseGenerator, Args

def squares(n):
    for i in range(n):
        yield i**2
        
squares_inputs = [
    Args(2),
    Args(5),
    Args(10),
]

### 
exo_squares = ExerciseGenerator(
    squares, squares_inputs, nb_examples=0)

###
exo_squares_maxed = ExerciseGenerator(
    squares, squares_inputs, nb_examples=0, max_iterations=5)


###
from itertools import count

exo_count_maxed = ExerciseGenerator(
    count, [Args()], nb_examples=0, max_iterations=5)



def squares_count():
    return (x**2 for x in count())

exo_squares_count_maxed = ExerciseGenerator(
    squares_count, [Args()], nb_examples=0, max_iterations=5)

    