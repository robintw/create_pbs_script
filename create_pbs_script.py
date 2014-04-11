#!/usr/local/bin/python
"""Create PBS batch scripts
by Robin Wilson (robin@rtwilson.com)

Usage:
    create_pbs_script [-m MEM] [-t TIME] PYTHONSCRIPT
    create_pbs_script [-m MEM] [-t TIME] PYTHONSCRIPT NAME


Options:
    -m --memory MEM  Set memory requirement
    -t --time TIME  Set walltime requirement

"""
import sys, os
from docopt import docopt


def create_pbs_script(pyfile, walltime="8:00:00", mem="15Gb", name=None):
    if name is None:
        pyfilename = os.path.splitext(pyfile)[0]
        name = "run_%s.pbs" % pyfilename

    if walltime is None:
        walltime = "8:00:00"
    elif "h" in walltime:
        walltime = walltime.replace("h", ":00:00")

    if mem is None:
        mem = "15Gb"

    contents = """#!/bin/bash
# PBS batch script automatically writen by create_pbs_script
# by Robin Wilson

# set resource requirements for job
#PBS -l walltime=%s
#PBS -l mem=%s

# Change to directory from which job was submitted.
# (The actual name is held in the PBS environment variable $PBS_O_WORKDIR)
cd $PBS_O_WORKDIR

module load python
module load gdal

python %s
""" % (walltime, mem, pyfile)

    with open(name, 'w') as f:
        f.write(contents)

    return name

if __name__ == "__main__":
    args = docopt(__doc__, version="create_pbs_script v1.0")
    print args
    print create_pbs_script(args['PYTHONSCRIPT'], walltime=args['--time'], mem=args['--memory'], name=args['NAME'])