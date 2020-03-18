from itertools import count

from nbautoeval import ExerciseGenerator, GeneratorArgs

def primes():
    cache_primes = set()
    
    # print(f"primes()")
    for n in count(2):
        # print(f"n={n}")
        for i in range(2, n):
            if i not in cache_primes:
                continue
            if n % i == 0:
                break
        else:
            cache_primes.add(n)
            yield n
            

primes_inputs = [
    GeneratorArgs(islice=(20,)),
    GeneratorArgs(islice=(None, 20, 2)),
    GeneratorArgs(islice=(100, 101)),
    GeneratorArgs(islice=(101, 102)),
    GeneratorArgs(islice=(1001, 1002)),
]

# max_iterations is mostly a provision to avoid endless loops
# as of 0.6 it seems like setting it to a big value like 10_000
# causes trouble, so ..
exo_primes = ExerciseGenerator(
    primes, primes_inputs, max_iterations=101,
    nb_examples=0,
)

exo_primes_no_limit = ExerciseGenerator(
    primes, primes_inputs, 
    nb_examples=0,
)