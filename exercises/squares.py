from nbautoeval import ExerciseGenerator, GeneratorArgs, IsliceRenderer, PPrintRenderer

# usual function that returns a generator
def squares(n):
    for i in range(n):
        yield i**2
        
squares_inputs = [
    GeneratorArgs(2),
    GeneratorArgs(5, islice=(1, 4)),
    GeneratorArgs(3, islice=(5,)),
    GeneratorArgs(10, islice=(2, 8, 3)),
    GeneratorArgs(4, islice=(4,)),
    GeneratorArgs(5, islice=(4,)),
    GeneratorArgs(10, islice=(0, 10)),
    GeneratorArgs(10, islice=(0, 5)),
    GeneratorArgs(10, islice=(0, 15)),
    GeneratorArgs(10, islice=(5, 15)),
    GeneratorArgs(10, islice=(4, 10, 4)),
    GeneratorArgs(10, islice=(4, 20, 4)),
    GeneratorArgs(10, islice=(5, 15, 5)),
    GeneratorArgs(10, islice=(5, 15, 3)),
    GeneratorArgs(10, islice=(15, 20)),
]


exo_squares = ExerciseGenerator(
    squares, squares_inputs, nb_examples=4,
    result_renderer=PPrintRenderer(width=30),
)


### same with max_iterations
exo_squares_maxed = ExerciseGenerator(
    squares, squares_inputs, 
    nb_examples=0, max_iterations=5,
    result_renderer=PPrintRenderer(width=30),
)


###
from itertools import count

simple_inputs = [
    GeneratorArgs(),
    GeneratorArgs(islice=(10, 12)),
]

exo_count_maxed = ExerciseGenerator(
    count, simple_inputs,
    nb_examples=0, max_iterations=5,
    result_renderer=PPrintRenderer(width=30),
)
