# -*- coding: utf-8 -*-
# # provide a workable class

####################
class Fifo:

    def __init__(self):
        self.items = []

    def __repr__(self):
        contents = join(["{}".format(i) for i in self.items])
        return f"<Fifo [{contents}]>"

    def incoming(self, incoming):
        self.items.append(incoming)

    def outgoing(self):
        if len(self.items) == 0:
            return None
        return self.items.pop(0)
    
    def __len__(self):
        return len(self.items)


# # create an exercise instance

from nbautoeval.exercise_class import ExerciseClass, ScenarioClass
from nbautoeval.args import Args

scenario1 = ScenarioClass(
    # arguments to the constructor
    Args(),
    # a list of expressions, with 
    # INSTANCE and CLASS replaced as appropriate
    "INSTANCE.incoming(1)",
    "INSTANCE.incoming(2)",
    "INSTANCE.outgoing()",
    "INSTANCE.incoming(3)",
    "INSTANCE.incoming(4)",
    "INSTANCE.outgoing()",
    "len(INSTANCE)"
)

scenario2 = ScenarioClass(
    Args(),
    "INSTANCE.outgoing()",
    "INSTANCE.incoming(1)",
    "INSTANCE.incoming(2)",
    "INSTANCE.incoming(3)",
    "INSTANCE.incoming(4)",
    "INSTANCE.outgoing()",
)    

exo_fifo = ExerciseClass (Fifo, [scenario1, scenario2],
                          layout='pprint')

if __name__ == '__main__':
    exo_fifo.correction(Fifo)

