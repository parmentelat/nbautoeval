#!/usr/bin/env python

# NOTE : tweak before use !!!

# this script was used once but is now obsolete
# as the traces now have gone to a json format
# overall logic should be mostly ok though

import sys

import re
import json
from pathlib import Path
from argparse import ArgumentParser
from typing import Tuple, Union, List, Iterator, Dict

Exoname = str                           # an exoname as per nbautoeval
Student = str                           # plain text from filename
Grade = Union[int, float]               # final output
Attempt = Tuple[Exoname, List[Grade]]   # temp data structure


def scan(root) -> Iterator[Tuple[Student, Path]]:
    """
    searches a whole directory to spot trace files
    discovers student names through a heuristic on filenames
    which is that on nbhosting we have
    blabla/students/studentname/coursename/.nbautoeval*
    """
    root = Path(root).resolve()
    # print(f"scanning {root=}")
    for trace in Path(root).glob("**/.nbautoeval.trace"):
        # retrieve student name as first level from root
        # student = trace.resolve().relative_to(root).parts[0]
        student = trace.resolve().parents[1].name
        # print(f"yielding {student=} and {trace=}")
        yield student, trace


def best_grades_from_trace(student, trace, quiz_exonames) -> Dict[Exoname, Grade]:
    """
    read one trace file and scans for provided exonames
    returns best grade for each exoname
    """
    student_attempts = {exoname: [] for exoname in quiz_exonames}
    with trace.open() as feed:
        for line in feed:
            record = json.loads(line)
            if record['type'] != 'quiz':
                continue
            exoname = record['exoname']
            if exoname not in student_attempts:
                continue
            if 'max_score' in record:
                k_gr, k_mgr = ('normalized_score', 'normalized_max_score')
            else:
                k_gr, k_mgr = ('score', 'max_score')
            gr, mgr = record[k_gr], record[k_mgr]
            attempt = (gr, mgr)
            student_attempts[exoname].append(attempt)
            # print(f"exo {exoname}, gr={gr} and mgr={mgr}")
    student_results = {}
    for exoname, attempts in student_attempts.items():
        if not attempts:
            print(f"WARNING student {student} has no records for {exoname}")
            continue
        # check consistency of mgr across all attempts
        mgrs = {attempt[1] for attempt in attempts}
        if len(mgrs) != 1:
            print(f"WARNING student {student} - cannot grade b/c of different max grades {mgrs}")
            continue
        student_results[exoname] = max(attempt[0] for attempt in attempts)
    return student_results


def all_grades_from_root(root, exonames) -> Dict[Student, Dict[Exoname, Grade]]:
    """
    returns final (max) grades from all trace files found in root
    """
    return {student: best_grades_from_trace(student, trace, exonames)
            for student, trace in scan(root)}


def main():
    parser = ArgumentParser()
    parser.add_argument("roots", metavar='roots', type=str, nargs="+",
                        help="root directories to search for .nbautoeval traces")
    parser.add_argument("-e", "--exo", dest="exonames", 
                        action='append', type=str,
                        help="the exonames we are interested in")
    parser.add_argument("-o", "--output",
                        help="filename to store as JSON")
    parser.add_argument("-v", "--verbose", action='store_true', default=False,
                        help="print on terminal even if -o is provided")
    args = parser.parse_args()

    roots = args.roots
    if not args.roots:
        parser.print_help()
        exit(1)

    # we assume one student appears in only one root
    student_grades = {}
    for root in roots:
        student_grades.update(all_grades_from_root(root, args.exonames))

    if args.output:
        with Path(args.output).open('w') as writer:
            writer.write(json.dumps(student_grades) + "\n")
    if not args.output or args.verbose:
        for student, grades in sorted(student_grades.items()):
            message = ""
            for exoname, grade in grades.items():
                message += f"{exoname}: {grade:.2f}"
            print(f"{student:^32}:  {message}")

if __name__ == '__main__':
    main()
