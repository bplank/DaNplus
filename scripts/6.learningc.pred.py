import os
import eval
import myutils
outDir = myutils.predDir + 'learningC/'
if not os.path.isdir(outDir):
    os.mkdir(outDir)

devs = ['news', 'reddit', 'twitter', 'arto']


for i in range(17):
    for training in ['deda', 'da']:
        name = 'learningC.' + training + '.' + str(i)
        modelPath = myutils.getModel(name)
        if modelPath == '':
            continue
        trainSize = (i+1) * 250
        for dev in devs:
            inFile = '../' + myutils.getDevFile(dev, 'multi')
            outFile = outDir  + dev + '.' + training + '.' + str(i)
            cmd = 'cd mtp && python3 predict.py ' + modelPath + ' ' + inFile
            cmd += ' ../' + outFile + ' --dataset DA --device 0 && cd ../'
            #if not os.path.isfile(outFile):
            print(cmd)


