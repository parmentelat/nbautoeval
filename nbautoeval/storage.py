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

def _storage_path():
    return _log_path().with_suffix(".json")


# ----------

def _log_message(exoname, message):
    """
    write a one-liner in the log file that contains
    timestamp unix-uid exoname <some message>
    """
    try:
        now = time.strftime("%D-%H:%M", time.localtime())
        uid = os.getuid()
        with _log_path().open('a') as log:
            line = f"{now} {uid} {exoname} {message}\n"
            log.write(line)
    except Exception as exc:
        print(f"nbautoeval could not _log_message {message} - {type(exc)} {exc}")


# ----------
def log_correction(exoname, success):
    """
    this is adapted to binary feedback (good or bad)
    """
    _log_message(exoname, "OK" if success else "KO")
    

def log_quiz(exoname, score, max_score, normalized_score, normalized_max_score):
    """
    this is adapted to quiz-like exercices that 
    come out with a score like 14 / 20
    """
    _log_message(exoname,
                 (f"{score}/{max_score} "
                  f"{normalized_score:.2f}/{normalized_max_score:.2f}"))


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
        
    
