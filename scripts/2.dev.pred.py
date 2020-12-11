import os
import myutils

def run(train, embeds, setting, dev, seed):
    trainName = '.'.join([train, embeds, setting, seed])
    modelPath = myutils.getModel(trainName)
    devFile = myutils.getDevFile(dev, setting)
    
    if not modelPath:
        #print("skipping .. no model found", file=sys.stderr) # push this error message up to myutils
        return
    outDir = myutils.predDir + train + '/'
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    outFile = outDir + setting + '.' + embeds + '.' + dev + '.' + seed

    predSet = 'DA'
    #if dev == 'german' or train == 'de':
    #    predSet = 'DE'
    cmd = 'cd mtp && python3 predict.py ' + modelPath + ' ../' + devFile + ' ../' + outFile + ' --dataset ' + predSet + ' --device 0 && cd ..'
    #if not os.path.isfile(outFile) or os.path.getsize(outFile) == 0:
    #    print(cmd)
    print(cmd)
    
if not os.path.isdir(myutils.predDir):
    os.mkdir(myutils.predDir)

for train in myutils.trains:
    for embed in myutils.embeds:
        for setting in myutils.settings:
            for dev in myutils.devs:
                for seed in myutils.seeds:
                    run(train, embed, setting, dev, seed)


