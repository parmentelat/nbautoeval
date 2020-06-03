# -*- coding: utf-8 -*-

# pylint: disable=c0111, w0703


# for logging
import os
import time
import json

from pathlib import Path

########## logging
def _log_path():
    """
    returns a Path object where to log attempts
    
    can be specified with env. variable NBAUTOEVAL_LOG
    defaults to $HOME/.nbautoeval
    """
    # use the env variable if set, or fallback to default
    from_env = os.environ.get('NBAUTOEVAL_LOG')
    
    result = Path(from_env) if from_env else Path.home() / ".nbautoeval"
    # we need to return a file and to make sure its dir. exists
    if result.is_dir():
        return result / ".nbautoeval"
    elif result.parent.is_dir():
        return result
    else:
        result.parent.mkdir(parents=True)
        return result

def _log2_path():
    return _log_path().with_suffix(".trace")

def _storage_path():
    return _log_path().with_suffix(".storage")

# historically for each attempt we stored in 
#    ~/.nbautoeval 
# a line with
# <date> <userid> <exoname> <details...>
# with details depending on the kind of exercise 
# * functions get a OK/KO, while
# * quizzes get details on the grade
# because this format has grown fragile it is recommended to read
#   ~/.nbautoeval.trace instead,
# which has the same info but in JSON format
# now, for compatibility we still store the old format
# but the way to compute this <userid> thingy is fragile too
# and it is no longer exposed in the json output anyway
# so from 1.1.6 we just write 'unknown-user' instead of userid

# ----------
# first-generation logging - for exercises initially
def _log_line(exoname, message):
    """
    write a one-liner in the log file that contains
    timestamp unix-uid exoname <some message>
    """
    try:
        now = time.strftime("%D-%H:%M", time.localtime())
        uid = 'unknown-user'
        with _log_path().open('a') as log:
            line = f"{now} {uid} {exoname} {message}\n"
            log.write(line)
    except Exception as exc:
        print(f"nbautoeval could not _log_line {message} - {type(exc)} {exc}")


# ----------
def log_correction(exoname, success):
    """
    this is adapted to binary feedback (good or bad)
    """
    _log_line(exoname, "OK" if success else "KO")
    

def log_quiz(exoname, score, max_score, normalized_score, normalized_max_score):
    """
    this is adapted to quiz-like exercices that 
    come out with a score like 14 / 20
    """
    _log_line(exoname, (f"{score}/{max_score} "
                        f"{normalized_score:.2f}/{normalized_max_score:.2f}"))

# ----------
# second-generation logging - one json record per line
# for a more flexible format
# for quizzes right now, would make sense to extend to exercises as well
# drop uid in the mix, it's just noise, this goes in $HOME already
def _log2_struct(exoname, type, struct: dict):
    # keep stuff in order
    stored = dict(
        exoname=exoname,
        type=type,
        time=time.strftime("%D-%H:%M:%S", time.localtime()))
    stored.update(struct)
    try:
        with _log2_path().open('a') as log:
            print(json.dumps(stored), file=log)
    except Exception as exc:
        print(f"nbautoeval could not _log_struct {struct} - {type(exc)} {exc}")


def log2_correction(exoname, *, success, **optional):
    """
    extensible json-based log for exercises
    """
    struct = dict(success=success)
    struct.update(optional)
    _log2_struct(exoname, 'exercise', struct)


def log2_quiz(exoname, *, attempt, max_attempts, score, max_score, **optional):
    """
    extensible json-based log about a quiz 
    with thorough details on that attempt
    """
    struct = dict(attempt=attempt, max_attempts=max_attempts,
                  score=score, max_score=max_score)
    struct.update(optional)
    _log2_struct(exoname, 'quiz', struct)

# ----------
def storage_read(exoname, attribute, default):
    try:
        with _storage_path().open() as feed:
            storage = json.loads(feed.read())
            return storage[exoname].get(attribute, default)
    except:
        return default
        
def storage_save(exoname, attribute, value):
    try:
        with _storage_path().open() as feed:
            storage = json.loads(feed.read())
    except:
        storage = {}
    
    if exoname not in storage:
        storage[exoname] = {}
    storage[exoname][attribute] = value
    
    with _storage_path().open('w') as writer:
        writer.write(json.dumps(storage))
        

def storage_clear(exoname):
    try:
        with _storage_path().open() as feed:
            storage = json.loads(feed.read())
    except:
        return
    if exoname not in storage:
        return

    del storage[exoname]
    
    with _storage_path().open('w') as writer:
        writer.write(json.dumps(storage))
        
    
