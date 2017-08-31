#test

import os.path
from os import listdir
from os.path import isfile, join

mypath = '/raid2/data/jenkinsjc/CSHL/jp2000_reduced/fluorescent/reduce_6/'




onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


onlyNumbers = []
for f in onlyfiles:
    onlyNumbers.append(int(f.split('.')[0]))
    

onlyNumbers.sort()

min_N = min(onlyNumbers)
max_N = max(onlyNumbers)

for i in range(min_N, max_N):
    a_file = mypath+str(i)+'.tif'
    if not(os.path.isfile(a_file) ):
        print("MISSING -> " + str(i))


