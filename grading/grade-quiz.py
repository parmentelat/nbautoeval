#!/usr/bin/env python

import re
import json
from pathlib import Path
from argparse import ArgumentParser
from typing import Tuple, Union, List, Iterator, Dict

Keyword = str                           # an exercise name as per nbautoeval
Student = str                           # plain text from filename
Grade = Union[int, float]               # final output
Attempt = Tuple[Keyword, List[Grade]]   # temp data structure

# stupid me... next time let's use a json format...

UID = r"[0-9]+"
KWD = r"[a-zA-Z0-9_-]+"
DATE = r"[0-9/:-]+"
SCORE = r"[0-9.-]+"
# for now this assumes a max_grade was used (parsed as mgr)
quiz_log_pattern = (
    rf"(?P<date>{DATE})\s(?P<uid>{UID})\s(?P<kwd>{KWD})\s"
    rf"(?P<sc>{SCORE})/(?P<msc>{SCORE})\s(?P<gr>{SCORE})/(?P<mgr>{SCORE})"
)

def scan(root) -> Iterator[Tuple[Student, Path]]:
    """
    searches a whole directory to spot logfiles
    discovers student names through a heuristic on filenames
    """
    root = Path(root).resolve()
    for log in Path(root).glob("**/.nbautoeval"):
        # retrieve student name as first level from root
        student = log.resolve().relative_to(root).parts[0]
        yield student, log


def best_grades_from_log(student, log, quiz_keywords) -> Dict[Keyword, Grade]:
    """
    read one log file and scans for provided keywords
    returns best grade for each keyword
    """
    student_attempts = {keyword: [] for keyword in quiz_keywords}
    with log.open() as feed:
        for line in feed:
            match = re.match(quiz_log_pattern, line)
            if not match:
                # as of this writing it could be wither
                # a regular non-quiz exercise result
                # or it could be the quiz has no max_grade defined
                continue
            keyword = match.group('kwd')
            if keyword not in student_attempts:
                continue
            gr, mgr = match.group('gr'), match.group('mgr')
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
    returns final (max) grades from all log files found in root
    """
    return {student: best_grades_from_log(student, log, keywords)
            for student, log in scan(root)}


def main():
    parser = ArgumentParser()
    parser.add_argument("keywords", metavar='keyword', type=str, nargs="+")
    parser.add_argument("-r", "--root", dest="roots",
                        action='append', type=str,
                        help="root directories to search for .nbautoeval logs")
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
            writer.write(json.dumps(student_grades))
    if not args.output or args.verbose:
        for student, grades in sorted(student_grades.items()):
            print(f"{student} -> {grades}")

if __name__ == '__main__':
    main()
