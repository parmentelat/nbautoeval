# -*- coding: utf-8 -*-

# pylint: disable=c0111, w0703


# for logging
import os
import os.path
import time

########## logging
def log_filename():
    """
    returns the filename where to log attempts
    can be specified with env. variable NBAUTOEVAL_LOG
    defaults to $HOME/.nbautoeval
    """
    # use the env variable if set, or fallback to default
    return os.environ.get('NBAUTOEVAL_LOG') \
        or os.path.join(os.getenv("HOME"), ".nbautoeval")

def log_correction(exoname, success):
    """
    write a one-liner in the log file that contains

    timestamp unix-uid exo-name {ok|ko}
    """
    try:
        now = time.strftime("%D-%H:%M", time.localtime())
        uid = os.getuid()
        message = "OK" if success else "KO"
        with open(log_filename(), 'a') as log:
            line = f"{now} {uid} {exoname} {message}\n"
            log.write(line)
    except Exception:
        # really not sure what to do then...
        pass
