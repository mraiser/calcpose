import subprocess
import csv
import json
import face_modifiers
import generate
from mhrc.JsonCall import JsonCall


def calcdelta(target, data, keys):
    delta = 0
    for key in keys:
        d = float(data[key]) - float(target[key])
        delta += (d * d)
    return delta


def optimize(target, keys, modifier, v, step, tolerance, shrinkage):
    generate.modify(modifier, v)
    data = generate.analyze()
    delta = calcdelta(target, data, keys)
    print("start "+modifier)
    print('start delta: '+str(delta))
    print("start v: "+str(v))
    lowv = v
    while abs(step) > tolerance:
        v = lowv + step
        generate.modify(modifier, v)
        nudata = generate.analyze()
        nudelta = calcdelta(target, nudata, keys)
        if nudelta > delta:
            step = (0 - step) * shrinkage
        elif nudelta == delta:
            print('No further effect detected, exit approach')
            break
        else:
            print(str(nudelta) + '/' + str(v) + '/' + str(step))
            lowv = v
            delta = nudelta
    generate.modify(modifier, lowv)
    nudata = generate.analyze()
    nudelta = calcdelta(target, nudata, keys)
    print(modifier+' FINAL SCORE: '+str(nudelta) + '/' + str(lowv))
    return lowv


def iterate(target, values, keys, step):
    n = 0
    done = {}
    while True:
        n += 1
        print("GEN: "+str(n))
        count = 0
        for modifier in values:
            if modifier not in done:
                v = values[modifier]
                generate.modify(modifier, v)
                data = generate.analyze()
                delta = calcdelta(target, data, keys)
                nuv = v + step
                generate.modify(modifier, nuv)
                nudata = generate.analyze()
                nudelta = calcdelta(target, nudata, keys)
                if nudelta >= delta:
                    nuv = v - step
                    generate.modify(modifier, nuv)
                    nudata = generate.analyze()
                    nudelta = calcdelta(target, nudata, keys)
                    if nudelta >= delta:
                        nuv = v
                if v != nuv:
                    count += 1
                else:
                    done[modifier] = True
                generate.modify(modifier, nuv)
                values[modifier] = nuv
        data = generate.analyze()
        delta = calcdelta(target, data, keys)
        print("Value: "+str(delta))
        print("Count: "+str(count))
        if count == 0:
            break


modifiers = face_modifiers.list_all()

inputdir = '/home/mraiser/PycharmProjects/calcpose/input/'
outputdir = '/home/mraiser/PycharmProjects/calcpose/processed/'
inputfile = 'y2.jpg'
outputfile = 'y2.csv'

b = True
if b:
    generate.reset_camera()
    generate.modify('macrodetails/Caucasian', 1)
    generate.modify('macrodetails/Gender', 0)

values = {}

b = False
if b:
    # To start with a previously derived value set
    with open('processed/y2-9b.json') as json_file:
        values = json.load(json_file)

for modifier in modifiers:
    v = 0.0
    if modifier in values:
        v = values[modifier]
    else:
        values[modifier] = v
    generate.modify(modifier, v)

generate.scan(inputdir+inputfile)
target = generate.read_csv(outputdir+outputfile)

b = True
if b:
    # Match the exact head position in the target photo
    # FIXME - There is no rot Z in MH
    tz = generate.approach(float(target[' pose_Tz']), 7, 0.1, True, ' pose_Tz', 'z', generate.zoom, 0.1, 0.9)
    ty = generate.approach(float(target[' pose_Ty']), 0.9, -0.1, True, ' pose_Ty', 'y', generate.trans, 0.1, 0.9)
    tx = generate.approach(float(target[' pose_Tx']), 0, -0.1, True, ' pose_Tx', 'x', generate.trans, 0.1, 0.9)
    rx = generate.approach(float(target[' pose_Rx']), 0, 0.01, False, ' pose_Rx', 'x', generate.rot, 0.01, 0.9)
    ry = generate.approach(float(target[' pose_Ry']), 0, 0.01, False, ' pose_Ry', 'y', generate.rot, 0.01, 0.9)
    rz = generate.approach(float(target[' pose_Rz']), 0, 0.01, False, ' pose_Rz', 'z', generate.rot, 0.01, 0.9)

    # tx=-0.022129047311218474 ty=-0.20758200697615223 tz=4.831655557931238 rx=0.04 ry=-0.20758200697615223 rz=0.0
    print(
        'tx=' + str(tx) + ' ty=' + str(ty) + ' tz=' + str(tz) + ' rx=' + str(rx) + ' ry=' + str(ty) + ' rz=' + str(rz))

facekeys = []
for i in range(1, 68):
    # facekeys.append(' x_' + str(i))
    # facekeys.append(' y_' + str(i))
    facekeys.append(' X_' + str(i))
    facekeys.append(' Y_' + str(i))
    facekeys.append(' Z_' + str(i))

b = False
if b:
    # Attempt #1.
    # Gets kinda close, maybe?
    # Starts getting really weird if you run this multiple times progressively against the previous result values
    step = 0.1
    for x in range(1,11):
        print("STEP "+str(x)+" ("+str(step)+")")
        iterate(target, values, facekeys, step)
        step *= 0.9
        print("{")
        for key in values:
            print('"'+key+'": '+str(values[key])+',')
        print("}")

b = True
if b:
    # Attempt #2
    # Really, really, ridiculously slow.
    # Seems pretty OK, actually
    facekeys = []
    for i in range(1, 68):
        facekeys.append(' X_' + str(i))
        facekeys.append(' Y_' + str(i))
        facekeys.append(' Z_' + str(i))

    tolerance = 0.01
    shrinkage = 0.9
    step = 0.1
    for i in range(10):
        print('GEN '+str(i)+' begin')
        changecount = 0
        for modifier in modifiers:
            if modifier in values:
                v = values[modifier]
            else:
                v = 0
            nuv = optimize(target, facekeys, modifier, v, step, tolerance, shrinkage)
            if nuv != v:
                print(modifier+': '+str(nuv))
                values[modifier] = nuv
                changecount += 1

        print("{")
        for key in values:
            print('"'+key+'": '+str(values[key])+',')
        print("}")

        print('GEN '+str(i)+' end')
        if changecount == 0:
            print("No changes in this GEN, exiting")
            break
        else:
            print("Number of changes: "+str(changecount))

        step *= 0.9
