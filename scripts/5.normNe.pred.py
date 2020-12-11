import os
import myutils

def run(train, embeds, setting, dev, seed, norm):
    trainName = '.'.join([train, embeds, setting, seed])
    modelPath = myutils.getModel(trainName)
    devFile = myutils.getDevFile(dev, setting + '-' + norm)

    outDir = 'predictions/' + train + '/'
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    outFile = outDir + setting + '.' + embeds + '.' + dev + '.' + norm + '.' + seed 

    predSet = 'DA'
    if dev == 'german':
        predSet = 'DE'
    cmd = 'cd mtp && python3 predict.py ' + modelPath + ' ../' + devFile + ' ../' + outFile + ' --dataset ' + predSet + ' --device 0 && cd ..'
    #if not os.path.isfile(outFile):
    #    print(cmd)
    print(cmd)
    
if not os.path.isdir('predictions'):
    os.mkdir('predictions')

for train in ['da', 'deda']:
    for norm in ['predNorm', 'goldNorm']:
        for dev in ['twitter', 'arto']:
            for seed in myutils.seeds:
                run(train, 'ml', 'multi', dev, seed, norm)


