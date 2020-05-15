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

Keyword = str                           # an exercise name as per nbautoeval
Student = str                           # plain text from filename
Grade = Union[int, float]               # final output
Attempt = Tuple[Keyword, List[Grade]]   # temp data structure


def scan(root) -> Iterator[Tuple[Student, Path]]:
    """
    searches a whole directory to spot trace files
    discovers student names through a heuristic on filenames
    """
    root = Path(root).resolve()
    for trace in Path(root).glob("**/.nbautoeval.trace"):
        # retrieve student name as first level from root
        student = trace.resolve().relative_to(root).parts[0]
        yield student, trace


def best_grades_from_trace(student, trace, quiz_keywords) -> Dict[Keyword, Grade]:
    """
    read one trace file and scans for provided keywords
    returns best grade for each keyword
    """
    student_attempts = {keyword: [] for keyword in quiz_keywords}
    with trace.open() as feed:
        for line in feed:
            record = json.loads(line)
            if record['type'] != 'quiz':
                continue
            keyword = record['exoname']
            if keyword not in student_attempts:
                continue
            if 'max_score' in record:
                k_gr, k_mgr = ('normalized_score', 'normalized_max_score')
            else:
                k_gr, k_mgr = ('score', 'max_score')
            gr, mgr = record[k_gr], record[k_mgr] 
            attempt = (gr, mgr)
            student_attempts[keyword].append(attempt)
            # print(f"exo {keyword}, gr={gr} and mgr={mgr}")
    student_results = {}
    for keyword, attempts in student_attempts.items():
        if not attempts:
            print(f"WARNING student {student} has no records for {keyword}")
            continue
        # check consistency of mgr across all attempts
        mgrs = {attempt[1] for attempt in attempts}
        if len(mgrs) != 1:
            print(f"WARNING student {student} - cannot grade b/c of different max grades {mgrs}")
            continue
        student_results[keyword] = max(attempt[0] for attempt in attempts)
    return student_results


def all_grades_from_root(root, keywords) -> Dict[Student, Dict[Keyword, Grade]]:
    """
    returns final (max) grades from all trace files found in root
    """
    return {student: best_grades_from_trace(student, trace, keywords)
            for student, trace in scan(root)}


def main():
    parser = ArgumentParser()
    parser.add_argument("keywords", metavar='keyword', type=str, nargs="+")
    parser.add_argument("-r", "--root", dest="roots",
                        action='append', type=str,
                        help="root directories to search for .nbautoeval traces")
    parser.add_argument("-o", "--output",
                        help="filename to store as JSON")
    parser.add_argument("-v", "--verbose",
                        help="print on terminal even if -o is provided")
    args = parser.parse_args()

    roots = args.roots
    if not args.roots:
        parser.print_help()
        exit(1)

    # we assume one student appears in only one root
    student_grades = {}
    for root in roots:
        student_grades.update(all_grades_from_root(root, args.keywords))
    
    if args.output:
        with Path(args.output).open('w') as writer:
            writer.write(json.dumps(student_grades) + "\n")
    if not args.output or args.verbose:
        for student, grades in sorted(student_grades.items()):
            print(f"{student} -> {grades}")

if __name__ == '__main__':
    main()
