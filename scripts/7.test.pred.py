import os
import eval
import myutils

outDir = myutils.predDir + 'test/'
if not os.path.isdir(outDir):
    os.mkdir(outDir)

for embed in myutils.embeds:
    for seed in myutils.seeds:
        for test in myutils.devs:
            name = '.'.join(['test', test, embed, seed])
            modelPath = myutils.getModel('deda.' + embed + '.multi.' + seed)
            inFile = '../' + myutils.getTestFile(test, 'multi')
            outFile = '../predictions/test/' + name
    
            predSet = 'DA'
            if test == 'german':
                predSet = 'DE'
            cmd = 'cd mtp && python3 predict.py ' + modelPath + ' ' + inFile + ' ' 
            cmd += outFile + ' --dataset ' + predSet + ' --device 0 && cd ../'
            print(cmd)
    
        # Normalization experiments
        for test in myutils.devs[-2:]:
            name = '.'.join(['test', test, embed, 'predNorm', seed])
            modelPath = myutils.getModel('deda.' + embed + '.multi.' + seed)
            if modelPath == '':
                continue
            inFile = '../' + myutils.getTestFile(test, 'multi-predNorm')
            outFile = '../predictions/test/' + name
            
            predSet = 'DA'
            cmd = 'cd mtp && python3 predict.py ' + modelPath + ' ' + inFile + ' ' 
            cmd += outFile + ' --dataset ' + predSet + ' --device 0 && cd ../'
            print(cmd)

