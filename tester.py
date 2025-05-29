#make classes for extra class# make version for proper programs
#es and then just parse them in
 
import copy
import json
import sys
import subprocess
import types
import pytest

def program(correct=False,fixed=False):
    if not fixed and not correct:
        flag = ''
    elif fixed and not correct: flag = "--fixed"
    else: flag = "--correct"
    return flag


def prettyprint(o):
    if isinstance(o, types.GeneratorType):
        return("(generator) " + str(list(o)))
    else:
        return(str(o))


if __name__ == "__main__":
    algo = sys.argv[1]
    working_file = "python_testcases/"+"test_"+algo+".py"

    #Check buggy Python code
    if len(sys.argv)<3:
        print("**Buggy Program**")
        subprocess.run(["python", "-m", "pytest --tb=short -q", working_file])

    else: 
        flag = sys.argv[2]

        if flag=="--fixed":
            # check Fixed Python code (by agent)
            print("**Fixed Program**")
            subprocess.run(["python", "-m", "pytest", flag, working_file])

        
        if flag=="--correct":    
            ## check correct Python code (already given)
            print("**Correct Program**")
            subprocess.run(["python", "-m", "pytest", flag, working_file])

    