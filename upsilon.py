#!/usr/local/bin/python3
import json
import sys
from datetime import datetime

weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', "Sat", "Sun"]

yeses = ['y', 'Y', 'yes', 'Yes']

'''
entrydate : str  y-m-d hour
aliases : list
age : int
gender : console forces enum
general ethnicity
intelligence : int(1, 10)
hair :
eyes :
skin :
affiliation : (enforced)
description : long string
'''

def writejson(jsonobj, fout_):
    json.dump(jsonobj, fout_)



def printprofile(jsobj, name):
    if not name in jsobj:
        print("no entry for", name, "found")
        return
    js = jsobj[name]
    print('=' * 20)
    print()
    print(js['entrydate'], '\n')
    print(name)
    print("aliases:", js['aliases'], '\n')
    print("age:", js['age'])
    print("gender:", js['gender'])
    print("ethnicity:", js['ethnicity'], '\n')
    print("intelligence:", js['intelligence'], '\n')
    print("hair:", js['hair'])
    print("eyes:", js['eyes'])
    print("skin:", js['skin'], '\n')
    print("affiliation:", js['affiliation'], '\n')
    print("description:", js['description'])
    print()
    print('=' * 20)
    print("\n\n\n")



def prompt_aliases(js):
    print("enter aliases:")
    aliases = []
    while True:
        s = input()
        if s == "":
            break
        aliases.append(s)
    js['aliases'] = aliases

def prompt_age(js):
    print("enter age:")
    while True:
        age = input()
        if not age.isdigit() or int(age) < 0:
            print("please enter an integer >= 0")
        else:
            js['age'] = int(age)
            break

def prompt_gender(js):
    print("enter gender:")
    while True:
        gender = input()
        if gender in ["male", "female", "other"]:
            js['gender'] = gender
            break
        else:
            print('invalid gender, valids are: male, female, other')

def prompt_ethnicity(js):
    print('enter ethnicity:')
    js['ethnicity'] = input()

def prompt_intelligence(js):
    print('enter intelligence:')
    while True:
        intel = input()
        if intel.isdigit():
            if 1 <= int(intel) <= 10:
                js['intelligence'] = int(intel)
                break
        else:
            print('must be integer between 1 and 10 inclusive')

def prompt_hair(js):
    print('enter hair description:')
    js['hair'] = input()

def prompt_eye(js):
    print('enter eye description:')
    js['eyes'] = input()

def prompt_skin(js):
    print('enter skin colour:')
    js['skin'] = input()

def prompt_affiliation(js):
    print('enter affiliation:')
    js['affiliation'] = input()

def prompt_description(js):
    print('enter further description:')
    js['description'] = input()



def addprofile(jsobj, name):

    if name in jsobj:
        print("Warning: entry '%s' exists. Do you wish to overwrite? y/n" % name)
        if not input() in yeses:
           return

    print(name)
    js = jsobj[name] = {}

    js['entrydate'] = ''

    prompt_aliases(js)
    prompt_age(js)
    prompt_gender(js)
    prompt_ethnicity(js)
    prompt_intelligence(js)
    prompt_hair(js)
    prompt_eye(js)
    prompt_skin(js)
    prompt_affiliation(js)
    prompt_description(js)

    dt = datetime.now()
    js['entrydate'] = '%d-%d-%d %s %d:%d' % (dt.year, dt.month, dt.day, weekdays[dt.weekday()], dt.hour, dt.minute)

    print("added", name, "to epsilon\n\n")


def editprofile(jsobj, name):

    if not name in jsobj:
        print("no such entry '%s'\n" % name)
        return

    print("Editing", split[1], "\n")

    js = jsobj[name]

    while True:
        sys.stdout.write("epsilon " + path + ("  edit %s " % name) + "\u001B[32m ε \u001B[0m")
        sys.stdout.flush()
        ln = input()

        if ln == "exit":
            return
        elif ln == "ls":
            print()
            for j in js:
                print(j)
            print()
            continue

        if ln in js:
            if ln == 'entrydate':
                print('cannot edit entrydate like this')
                continue
            global needsave
            needsave = True
            eval('prompt_' + ln + '(js)')
        else:
            print("invalid parameter, type 'ls' for all parameters")


if len(sys.argv) == 1:
    print("please enter input file")
    exit(0)

path = sys.argv[1]

fin = None
obj = None

try:
    fin = open(path, 'r')
except FileNotFoundError:
    print("File does not exist, create new one? y/n")
    if input() in yeses:
        fin = open(path, 'w')
        fin.write('{}')
        fin.close()
        fin = open(path, 'r')
    else:
        exit(0)

try:
    obj = json.load(fin)
except json.decoder.JSONDecodeError:
    print("Epsilon: error parsing json file", file=sys.stderr)
    exit(1)

needsave = False

while True:
    sys.stdout.write("epsilon " + path + "\u001B[32m ε \u001B[0m")
    sys.stdout.flush()
    line = input()
    split = line.split(' ', 1)
    # // where is the goddamn switch case?

    if split[0] in ['cls', 'clr', 'clear']:
        print("\033[2J")
        sys.stdout.write("\033[1;1H")
        sys.stdout.flush()
    elif split[0] == 'exit':
        if needsave:
            print("Do you wish to save? y/n")
            if input() in yeses:
                writejson(obj, open(sys.argv[1], 'w'))
                print('Saved')
        print("Epsilon Exiting...")
        exit(0)
    elif split[0] == 'ls':
        for i in sorted(obj.keys()):
            print(i)
    elif split[0] in ['open', 'access']:
        if len(split) == 1:
            print("what do you want to access?")
        else:
            print("Accessing", split[1], "\n\n\n")
            printprofile(obj, split[1])
    elif split[0] == 'add':
        if len(split) == 1 or split[1] == "":
            print("what entry name do you want to add?")
        else:
            needsave = True
            print("Adding", split[1], "\n")
            addprofile(obj, split[1])
    elif split[0] == 'edit':
        if len(split) == 1 or split[1] == "":
            print("which entry to you want to edit?")
        else:
            editprofile(obj, split[1])
    elif split[0] == 'save':
        needsave = False
        fout = open(sys.argv[1], 'w')
        writejson(obj, fout)
        print("saved")
        fout.close()
    elif split[0] == 'saveas':
        needsave = False
        if len(split) == 1:
            print("please enter target file")
            continue
        fout = open(split[1], 'w')
        writejson(obj, fout)
        print("saved as", split[1])
        fout.close()


