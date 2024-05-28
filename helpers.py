# libhelpers by Jack Anderson
# helper functions
import random
import time
import math
from os import system, name

# clear screen for both platforms, windows nt uses cls, unix uses clear
def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")

# take a number as input, make sure it fits inside the index of arr given
def findex(ind, arr):
    maxi = len(arr)-1
    if ind > maxi:
        return findex((ind-maxi)-1, arr)
    else:
        return ind
# safe indexof, find obj in arr
def indexOf(obj, arr):
    if obj in arr:
        return arr.index(obj)
    else:
        return -1     
      
# forced non empty string input
def sinput(prompt):
    i = str(input(prompt))
    if i == "":
        return sinput(prompt)
    return i

def flip(bit):
    if bit == 1:
        return 0
    else:
        return 1
# forced input takes a list of options that must match, or rerun input
def finput(prompt, options, lower=True): 
    # ensure options are all lowercase
    if(lower == True):
        o = []
        for opt in options:
            o.append(opt.lower())
        options = o
    
    # get input and ensure is allowed
    i = str(input(prompt))
    if(lower == True):
        i = i.lower()
        
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
