import generate
import json
import os
import shutil

homedir = '/home/mraiser/PycharmProjects/calcpose/'
outputdir = homedir+'output/'
number_of_samples = 500
randomness = 1.0 / 3.0
symmetry = 0.75

if os.path.isdir(outputdir):
    shutil.rmtree(outputdir)
os.mkdir(outputdir)

b = False
if b:
    # generate headshot csv
    # rename xyz.csv to headshot.csv
    generate.reset_camera()
    generate.trans('y', 0.5)
    val = {}
    generate.reset_human(val)
    generate.set_values(val)
    generate.snap()
    generate.scan()

for num in range(number_of_samples):
    print(num)
    filename = outputdir + str(num)

    generate.reset_camera()
    generate.trans('y', 0.5)

    val = {}
    generate.random_human(val, randomness, symmetry)
    generate.set_values(val)
    with open(filename+'.json', 'w') as outfile:
        json.dump(val, outfile)

    b = False
    if b:
        # reposition relative to headshot.csv
        target = generate.read_csv(fname=homedir+'processed/headshot.csv')
        tz = generate.approach(float(target[' pose_Tz']), 7, 1, True, ' pose_Tz', 'z', generate.zoom, 1, 0.5)
        ty = generate.approach(float(target[' pose_Ty']), 0.9, -1, True, ' pose_Ty', 'y', generate.trans, 1, 0.5)

    generate.random_headshot_pose()

    fname = filename + '.jpg'
    generate.snap(fname)

    b = True
    if b:
        generate.scan(fname)
        s = homedir+'processed/' + str(num)
        os.rename(s + '.csv', filename + '.csv')
        os.remove(s + '.jpg')
        os.remove(s + '.hog')
        os.remove(s + '_of_details.txt')
        shutil.rmtree(s + '_aligned')

