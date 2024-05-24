# libhelpers by Jack Anderson
# helper functions
import random
import time
import math

# forced input takes a list of options that must match, or rerun input
def finput(prompt, options):
    # ensure options are all lowercase
    o = []
    for opt in options:
        o.append(opt.lower())
    options = o
    
    # get input and ensure is allowed
    i = str(input(prompt)).lower()
    if not i in options:
        return finput(prompt, options)
    else:
        return i
    
def log(text):
    print(f"[euchre] {text}")

def generate_id():
    return math.floor(time.time() * random.random())

# Ensure a unique random number within range, given an array, reps, of used numbers. 
# Return tuple of the number and reps array
def urand(low, high, reps):
    r = random.randint(low, high)
    if r in reps:
        return urand(low, high, reps)
    reps.append(r)
    return r, reps
