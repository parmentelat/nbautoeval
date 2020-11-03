from nbautoeval import ExerciseClass, Args, ClassScenario, ClassExpression, ClassStatement


# provide a workable class

####################
class Fifo:

    def __init__(self):
        self.items = []
        
    # see the check_init flag below 
    def __repr__(self):
        contents = ", ".join(str(item) for item in self.items)
        return f"[Fifo {contents}]"

    def incoming(self, incoming):
        self.items.append(incoming)

    def outgoing(self):
        if len(self.items) == 0:
            return None
        return self.items.pop(0)
    
    def __len__(self):
        return len(self.items)


#####
# define 2 flavours of the same exercise

# I: for newbies
# if like me you like to have students code their own stack the very first day
# at a point where __repr__() is not yet mastered, then the way ExerciseFunction
# by default checks for objects status cannot work well, since it does rely on repr()
# 
# you can still come up with the simplest assignment ever, 
# using check_init=True that by-passes checks after the first (initialization) step
# you must refrain from using Statements though in this case, because Statements
# are also checked using repr() 


exo_fifo_newbies = ExerciseClass(
    Fifo,
    [
        ClassScenario(
            Args(),
            ClassExpression("INSTANCE.incoming(1)"),
            ClassExpression("INSTANCE.outgoing()"),
        ),
        ClassScenario(
            Args(),
            ClassExpression("INSTANCE.incoming(1)"),
            ClassExpression("INSTANCE.incoming(2)"),
            ClassExpression("INSTANCE.outgoing()"),
            ClassExpression("INSTANCE.outgoing()"),
        ),
        ],
    check_init=False, nb_examples=0)
    
    

# a more realistic one
# this one will require the student to write a repr() 
# that exactly matches the official implementation

scenario1 = ClassScenario(
    # arguments to the constructor
    Args(),
    # a list of expressions, with 
    # INSTANCE and CLASS replaced as appropriate
    ClassExpression("INSTANCE.incoming(1)"),
    ClassExpression("INSTANCE.incoming(2)"),
    ClassExpression("INSTANCE"),
    # same than "INSTANCE" but with a slightly different display
    ClassExpression("repr(INSTANCE)"),
    ClassStatement("INSTANCE"),
    ClassExpression("INSTANCE.outgoing()"),
    ClassExpression("INSTANCE.incoming(3)"),
    ClassExpression("INSTANCE.incoming(4)"),
    ClassExpression("INSTANCE.outgoing()"),
    ClassExpression("len(INSTANCE)"),
)

scenario2 = ClassScenario(
    Args(),
    "INSTANCE.outgoing()",
    "INSTANCE.incoming(1)",
    "INSTANCE.incoming(2)",
    "INSTANCE.incoming(3)",
    "INSTANCE.incoming(4)",
    "INSTANCE.outgoing()",
)    

exo_fifo = ExerciseClass(
    Fifo, [scenario1, scenario2], check_init=False, obj_name='F')

if __name__ == '__main__':
    exo_fifo.correction(Fifo)

