import itertools

from nbautoeval import ExerciseGenerator, GeneratorArgs, PPrintRenderer

def differential(iterator):
    previous = next(iterator)
    while True:
        current = next(iterator)
        yield current - previous
        previous = current


def squares():
    return (i**2 for i in itertools.count())

differential_args = [
    GeneratorArgs(itertools.count(), islice=(10,)),
    GeneratorArgs(squares(), islice=(10,)),
]

exo_differential = ExerciseGenerator(
    differential, differential_args,
    copy_mode='tee',  # this is the broken piece in 0.6.1
    max_iterations=20,
    result_renderer=PPrintRenderer(width=20),
    
)
