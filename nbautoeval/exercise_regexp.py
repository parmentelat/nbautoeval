# -*- coding: utf-8 -*-

# pylint: disable=c0111, r1705, w0703


import re

from .exercise_function import ExerciseFunction

DEFAULT_MATCH_MODE = 'match'

class ExerciseRegexp(ExerciseFunction):
    """
    With these exercises the students are asked to write a regexp
    which is transformed into a function that essentially
    takes an input string and returns a boolean
    that says if the *whole* string matches or not
    """
    
    def regexp_to_solution(self, regexp, match_mode):
        def solution(string):
            if match_mode in ('match', 'search'):
                if match_mode == 'match':
                    match = re.match(regexp, string)
                else:
                    match = re.search(regexp, string)
                if not match:
                    return False
                else:
                    # xxx this is wrong ! matching section
                    # won't have the metachars in incoming pattern
                    return match.group(0) == string
            # findall returns strings, while finditer returns match instances
            elif match_mode == 'findall':
                return re.findall(regexp, string)
            elif match_mode == 'finditer':
                return [match.span()
                        for match in re.finditer(regexp, string)]
            return None
        return solution

    def __init__(self, name, regexp, inputs,
                 *args, match_mode=DEFAULT_MATCH_MODE, **keywords):
        """
        a regexp exercise is made with
        . a user-friendly name
        . a regexp pattern for the solution
        . a list of inputs on which to run the regexp
        . match_mode is either 'match', 'search' or 'findall'
        . additional settings from ExerciseFunction
        """
        solution = self.regexp_to_solution(regexp, match_mode)
        super().__init__(solution, inputs, *args, **keywords)
        self.regexp = regexp
        self.name = name
        self.match_mode = match_mode
        # it never makes sense to show the function name
        # that would always be 'solution' anyways
        self.call_renderer.show_function = False

    def correction(self, student_regexp):               # pylint: disable=w0221
        student_solution = self.regexp_to_solution(student_regexp, self.match_mode)
        return ExerciseFunction.correction(self, student_solution)
    
    @property
    def column_headers(self):
        return (self._column_headers if self._column_headers is not None 
            else ('chaîne', 'match ?', 'obtenu'))
    

##############################
class ExerciseRegexpGroups(ExerciseRegexp):
    """
    With these exercises the students are asked to write a regexp
    with a set of specified named groups
    a list of these groupnames needs to be passed to construct the object

    the regexp is then transformed into a function that again
    takes an input string and either a list of tuples
    (groupname, found_substring)
    or None if no match occurs
    """

    @staticmethod
    def extract_group(match, group):
        try:
            return group, match.group(group)
        except Exception:
            return group, "Undefined"

    def regexp_to_solution(self, regexp, match_mode):
        groups = self.groups
        if match_mode != 'match':
            # only tested with 'match' so far
            print(f"WARNING: ExerciseRegexpGroups : "
                  f"match_mode {match_mode} not yet implemented")
        def solution(string):
            if match_mode in ('match', 'search'):
                if match_mode == 'match':
                    match = re.match(regexp, string)
                else:
                    match = re.search(regexp, string)
                return match and [ExerciseRegexpGroups.extract_group(match, group)
                                  for group in groups]
            # findall returns strings, while finditer returns match instances
            elif match_mode == 'findall':
                return re.findall(regexp, string)
            elif match_mode == 'finditer':
                matches = re.finditer(regexp, string)
                return [[ExerciseRegexpGroups.extract_group(match, group)
                         for group in groups] for match in matches]
            return None
        return solution

    def __init__(self, name, regexp, groups, inputs,
                 *args, match_mode=DEFAULT_MATCH_MODE, **keywords):
        self.groups = groups
        super().__init__(name, regexp, inputs, *args, match_mode=match_mode, **keywords)

    @property
    def column_headers(self):
        return (self._column_headers if self._column_headers is not None 
            else ('chaîne', 'groupes', 'obtenu'))
