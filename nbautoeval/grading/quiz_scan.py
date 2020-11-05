"""
a command to produce quiz grades as a JSON file

inputs:
* roots: directories where to look for results
* -e option: names of the quizzes of interest

it will:
* search for .nbautoeval.trace files located anywhere under the provided roots
* then extract all recorded attempts and retains the best score
* and produce a json (if -o is used to chose a destination json file)
* otherwise a plain text summary is written on the terminal

WARNING:
it is assumed that .nbautoeval.trace is located in a user's homedir
so a heuristic is used to compute the student name from the
full path of the trace file, namely the basename of the parent directory
"""

import sys

import re
import json
from pathlib import Path
from argparse import ArgumentParser, RawTextHelpFormatter
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

    if root.is_file():
        if root.name != ".nbautoeval.trace":
            return
        trace = root
        student = trace.resolve().parents[1].name
        yield student, trace
        return

    for trace in Path(root).glob("**/.nbautoeval.trace"):
        # retrieve student name as first level from root
        # student = trace.resolve().relative_to(root).parts[0]
        student = trace.resolve().parents[1].name
        yield student, trace


def best_grades_from_trace(student, trace, quiz_exonames, ignore) -> Dict[Exoname, Grade]:
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
    student_results = {}
    for exoname, attempts in student_attempts.items():
        if not attempts:
            if not ignore:
                print(f"WARNING student {student} has no records for {exoname}")
            continue
        # check consistency of mgr across all attempts
        mgrs = {attempt[1] for attempt in attempts}
        if len(mgrs) != 1:
            if not ignore:
                print(f"WARNING student {student} - cannot grade b/c of different max grades {mgrs}")
            continue
        student_results[exoname] = max(attempt[0] for attempt in attempts)
    return student_results


def all_grades_from_root(root, exonames, ignore) -> Dict[Student, Dict[Exoname, Grade]]:
    """
    returns final (max) grades from all trace files found in root
    """
    return {student: best_grades_from_trace(student, trace, exonames, ignore)
            for student, trace in scan(root)}


def main():
    parser = ArgumentParser(epilog=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument("roots", metavar='roots', type=str, nargs="+",
                        help="root directories to search for .nbautoeval traces")
    parser.add_argument("-e", "--exo", dest="exonames",
                        action='append', type=str,
                        help="the exonames we are interested in")
    parser.add_argument("-i", "--ignore", action='store_true', default=False,
                        help="when set, remove warnings, and json only contains entries "
                             "for students who have at least one grade")
    parser.add_argument("-o", "--output",
                        help="filename to store as JSON")
    parser.add_argument("-v", "--verbose", action='store_true', default=False,
                        help="print on terminal even if -o is provided")
    args = parser.parse_args()

    roots = args.roots
    if not args.roots or not args.exonames:
        parser.print_help()
        exit(1)

    # we assume one student appears in only one root
    student_grades = {}
    for root in roots:
        student_grades.update(all_grades_from_root(root, args.exonames, args.ignore))

    if args.ignore:
        student_grades = { k: v for (k, v) in student_grades.items() if v}

    if args.output:
        with Path(args.output).open('w') as writer:
            writer.write(json.dumps(student_grades) + "\n")
    if not args.output or args.verbose:
        for student, grades in sorted(student_grades.items()):
            message = ""
            for exoname, grade in grades.items():
                message += f"{exoname}: {grade:.2f} "
            print(f"{student:^32}:  {message}")

if __name__ == '__main__':
    main()
