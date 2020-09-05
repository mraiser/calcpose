import face_modifiers
import subprocess
import csv
import json
import time
from mhrc.JsonCall import JsonCall
from random import seed
from random import random

seed(time.time_ns())


def reset_camera():
    jsc = JsonCall()
    jsc.setFunction("applyModifier")
    jsc.setParam("modifier", 'camera/reset')
    jsc.setParam("power", 0)
    jsc.send()


def modify(modifier, amt):
    jsc = JsonCall()
    jsc.setFunction("applyModifier")
    jsc.setParam("modifier", modifier)
    jsc.setParam("power", amt)
    jsc.send()


def zoom(axis, amt):
    jsc = JsonCall()
    jsc.setFunction("applyModifier")
    jsc.setParam("modifier", 'camera/zoom')
    jsc.setParam("power", amt)
    jsc.send()


def trans(axis, amt):
    jsc = JsonCall()
    jsc.setFunction("applyModifier")
    jsc.setParam("modifier", 'camera/trans_'+axis)
    jsc.setParam("power", amt)
    jsc.send()


def pan(axis, amt):
    jsc = JsonCall()
    jsc.setFunction("applyModifier")
    jsc.setParam("modifier", 'camera/pan_'+axis)
    jsc.setParam("power", amt)
    jsc.send()


def rot(axis, amt):
    jsc = JsonCall()
    jsc.setFunction("applyModifier")
    jsc.setParam("modifier", 'camera/rot_'+axis)
    jsc.setParam("power", amt)
    jsc.send()


def snap(filename='/home/mraiser/Desktop/xyz.jpg'):
    jsc = JsonCall()
    jsc.setFunction("applyModifier")
    jsc.setParam("modifier", 'camera/snapshot')
    jsc.setParam("filename", filename)
    jsc.setParam("power", 0)
    jsc.send()


def scan(fname = '/home/mraiser/Desktop/xyz.jpg'):
    fli = '/home/mraiser/Desktop/OPENCV/OpenFace/build/bin/FaceLandmarkImg'
    cmd = fli+' -f '+fname+' > /dev/null 2>&1'

    returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    if returned_value != 0:
        print('ERROR! returned value:', returned_value)


def read_csv(fname='/home/mraiser/PycharmProjects/calcpose/processed/xyz.csv'):
    with open(fname, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return row


def analyze():
    snap()
    scan()
    return read_csv()


def approach(target, v, step, cumulative, key, axis, action, tolerance, shrinkage):
    data = analyze()
    delta = float(data[key]) - target
    positive = delta > 0

    while abs(delta) > tolerance:
        v += step
        power = step
        if cumulative:
            power = v
        action(axis, power)
        nudata = analyze()
        nudelta = float(nudata[key]) - target
        nupositive = nudelta > 0
        print(nudata[key]+'/'+str(nudelta)+'/'+str(v))
        if positive != nupositive:
            step = (0-step)*shrinkage
            positive = nupositive
        elif abs(nudelta) > abs(delta):
            step = (0-step)*shrinkage
        elif nudelta == delta:
            print('No further effect detected, exit approach')
            v -= step
            power = 0 - step
            if cumulative:
                power = v
            action(axis, power)
            return v
        delta = nudelta
        # data = nudata

    return v


def random_float(bidirectional=False, max_deviation=1.0):
    v = random()
    if bidirectional:
        v = (2.0 * v) - 1.0
    v *= max_deviation
    return v


def is_bidirectional(modifier):
    b = modifier.endswith("|incr") \
                or modifier.endswith("|up") \
                or modifier.endswith("|forward") \
                or modifier.endswith("|convex") \
                or modifier.endswith("|uncompress") \
                or modifier.endswith("|out")
    return b


def random_face(values={}, max_deviation=0.25, symmetry=0.75):
    modifiers = face_modifiers.list_all()
    lefties = []
    for modifier in modifiers:
        v = random_float(is_bidirectional(modifier), max_deviation)
        values[modifier] = v
        i = modifier.index('/')
        if '/l-' in modifier:
            lefties.append(modifier)
    for lefty in lefties:
        i = lefty.index('/l-')
        righty = lefty.replace('/l-', '/r-')
        lval = values[lefty]
        rval = values[righty]
        rval = (symmetry * lval) + ((1.0 - symmetry) * rval)
        values[righty] = rval
    return values


def reset_face(values={}):
    return random_face(values, 0)


def set_values(values):
    modify('all', values)


def random_ethnicity(values):
    ethnicities = ['African', 'Asian', 'Caucasian']
    rand_ethnic = []
    i = int(random_float() * 3)
    rand_ethnic.append(ethnicities.pop(i))
    i = int(random_float() * 2)
    rand_ethnic.append(ethnicities.pop(i))
    rand_ethnic.append(ethnicities.pop(0))

    for i in range(3):
        values['macrodetails/'+rand_ethnic[i]] = random_float()
    return values


def reset_ethnicity(values):
    values['macrodetails/African'] = 1.0
    values['macrodetails/Asian'] = 0.5
    values['macrodetails/Caucasian'] = 1.0 / 3.0
    return values


def random_macro(values):
    values['macrodetails/Gender'] = random_float()
    values['macrodetails/Age'] = 0.36 + random_float(False, 0.64)  # Minimum 18 years old
    values['macrodetails-universal/Muscle'] = random_float()
    values['macrodetails-universal/Weight'] = random_float()
    values['macrodetails-height/Height'] = random_float()
    values['macrodetails-proportions/BodyProportions'] = random_float()
    return random_ethnicity(values)


def reset_macro(values):
    values['macrodetails/Gender'] = 0.5
    values['macrodetails/Age'] = 0.5
    values['macrodetails-universal/Muscle'] = 0.5
    values['macrodetails-universal/Weight'] = 0.5
    values['macrodetails-height/Height'] = 0.5
    values['macrodetails-proportions/BodyProportions'] = 0.5
    return reset_ethnicity(values)


def reset_human(val={}):
    reset_face(val)
    reset_macro(val)
    return val


def random_human(val={}, randomness=0.5, symmetry=0.75):
    random_face(val, randomness, symmetry)
    random_macro(val)
    return val


def random_headshot_pose(max_deviation=0.1):
    # FIXME - No way to rot Z in MH
    rot('x', random_float(True, max_deviation))
    rot('y', random_float(True, max_deviation))
