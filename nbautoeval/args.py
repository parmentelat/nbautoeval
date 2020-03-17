# -*- coding: utf-8 -*-

# pylint: disable=c0111, r1705

import copy
import pprint
import itertools
from collections.abc import Iterable, Iterator

from .helpers import custom_repr

####################
# From June 2016, this class should not need to be used directly
# as Args would allow to build it with a nicer interface
class ArgsTupleDict:
    """
    The most general form of a function argument list is made
    of a tuple and a dictionary

    Example:
    my_input = ArgsTupleDict((1, 2), {'a': []})
    my_input.call(foo)
    would then return the result of
    foo(1, 2, a=[])
    """
    def __init__(self, _args=None, _keywords=None):
        # expecting a tuple or a list
        self.args = _args if _args is not None else tuple()
        # expecting a dictionary
        self.keywords = _keywords if _keywords is not None else {}
        # can be overridden later on using 'render_function_name'
        self.function_name = None
        # can be overridden later on using 'render_prefix'
        self.prefix = ""
        self.postfix = ""


    def __repr__(self):
        result = f"<Args {self.prefix}{self.function_name}{self.args}{self.postfix} "
        if self.keywords:
            result += ("Keywords:" + 
                       ",".join(f"{k}={v}" for (k, v) in self.keywords.items()))
        result += ">"
        return result

    def call(self, function, debug=False):
        if debug:
            print(f"calling {function.__name__} *{self.args} **{self.keywords}")
        return function(*self.args, **self.keywords)

    def init_obj(self, klass, debug=False):
        if debug:
            print(f"creating object in class {klass.__name__}, *{self.args} **{self.keywords}")
        return klass(*self.args, **self.keywords)

    def call_obj(self, obj, methodname, debug=False):
        if debug:
            print(f"calling method {methodname} on object {obj} *{self.args} **{self.keywords}")
        method = getattr(obj, methodname)
        return method(*self.args, **self.keywords)

    def clone(self, copy_mode):
        "clone this input for safety"
        if copy_mode == 'shallow':
            return copy.copy(self)
        elif copy_mode == 'deep':
            return copy.deepcopy(self)
        else:
            return self
    
    # # rendering  
    def tokens(self):
        """
        returns a list of strings
        e.g. 
        Args(1, 2, x=1).tokens -> ['1', '2', 'x=1']
        """
        return ( [custom_repr(x) for x in self.args] 
                +[f"{k}={custom_repr(v)}" for (k, v) in self.keywords.items()])
        

# simplified for when no keywords are required
class Args(ArgsTupleDict):
    """
    In most cases though, we do not use keywords so it is more convenient to
    just pass a list of arguments

    Example:
    my_input = Args (1, 2, 3)
    my_input.call(foo)
    would then return the result of
    foo(1, 2, 3)

    """
    def __init__(self, *args, **kwds):
        # it is NOT *args here, this is intentional
        ArgsTupleDict.__init__(self, args, kwds)


class GeneratorArgs(Args):
    """
    GenArgs is like Args but designed for use 
    with an ExerciseGenerator
    
    See exercises/squares.py for an example of how to use it
    """
    def __init__(self, *args, islice=None, **kwds):
        super().__init__(*args, **kwds)
        self.islice = islice


    def call(self, function, debug=False):
        # call() already has it's contents converted
        # to a list because comparison of results alreqdy has taken place
        iterable = super().call(function)
        if not isinstance(iterable, Iterable):
            raise TypeError(f"not an iterable! received a {type(iterable).__name__} instance: {iterable}")
        if not self.islice:
            return iterable
        return list(itertools.islice(iterable, *self.islice))


    # handles iterator when part of self.args
    # this is a part of aborted 0.6.1
    # intention was to be smart about copying iterators
    # but that did not work out too well
    # kept this code for future reference only
    # but it not used be default with 0.6.2 version
    def copy_for_tee(self, copy_mode):
        copy1, copy2 = type(self)(), type(self)()
        for att in ('keywords', 'function_name'):
            setattr(copy1, att, copy.copy(getattr(self, att)))
            setattr(copy2, att, copy.copy(getattr(self, att)))
        a1, a2 = [], [] 
        for arg in self.args:
            if not isinstance(arg, Iterator):
                a1.append(copy.copy(arg))
                a2.append(copy.copy(arg))
            else:
                c1, c2 = itertools.tee(arg, 2)
                a1.append(c1)
                a2.append(c2)
        copy1.args = tuple(a1)
        copy2.args = tuple(a2)
        return copy1, copy2
    