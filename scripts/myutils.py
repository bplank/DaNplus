import matplotlib.pyplot as plt
import matplotlib as mpl
from pprint import pprint
import os
import eval
import statistics
import sys

trains = ['da', 'deda', 'de']
embeds = ['ml','da']
settings = ['single-merged', 'multi', 'multilabel']
#settomgs = ['single', 'single-crf', 'single-merged', 'multi', 'multilabel']
devs = ['german', 'news', 'reddit', 'twitter', 'arto']
seeds = ['1', '2', '3']
predDir = 'predictions/'

plt.style.use('scripts/niceGraphs.mplstyle')
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"] 
colors = colors + colors

def setTicks(ax, labels, rotation = 0):
    ticks = []
    for i in range (len(labels)):
        ticks.append(i + .5)

    ax.xaxis.set_major_locator(mpl.ticker.LinearLocator(len(labels)+1))
    ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator(ticks))

    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(mpl.ticker.FixedFormatter(labels))

    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('right')
        tick.label1.set_rotation(rotation)

def getDevFile(devDomain, devSetting):
    devFile = 'data/da_' + devDomain + '_dev.tsv'

    if devDomain == 'german':
        devFile = 'data/de_news_dev.tsv'
    if 'goldNorm' in devSetting:
        devFile = devFile.replace('.tsv', '_goldNorm.tsv')
    if 'predNorm' in devSetting:
        devFile = devFile.replace('.tsv', '_predNorm.tsv')
    if devSetting in ['multilabel', 'single-merged']:
        devFile = devFile.replace('.tsv', '_mh.tsv')

    if devFile == '':
        print("error, dev not found: " + devFile, file=sys.stderr)
        return
    return devFile

def getTestFile(testDomain, testSetting):
    testFile = 'data/da_' + testDomain + '_test.tsv'

    if testDomain == 'german':
        testFile = 'data/de_news_test.tsv'

    if 'goldNorm' in testSetting:
        testFile = testFile.replace('.tsv', '_goldNorm.tsv')
    if 'predNorm' in testSetting:
        testFile = testFile.replace('.tsv', '_predNorm.tsv')
    if testSetting in ['multilabel', 'single-merged']:
        testFile = testFile.replace('.tsv', '_mh.tsv')

    if testFile == '':
        print("error, test not found: " + testFile, file=sys.stderr)
        return
    return testFile

def writeJson(data, name, params):
    jsonPath = 'configs/' + name + '.json'
    with open(jsonPath, 'wt') as out:
        pprint(data, stream=out)
    cmd = 'cd mtp && python3 train.py --parameters_config ' + params
    cmd += ' --dataset_config ../' + jsonPath
    cmd += ' --name ' + name + ' --device 0 && cd ../'
    modelDir = 'mtp/logs/' + name + '/'
    metricsExist = False
    if os.path.isdir(modelDir):
        for subDir in os.listdir(modelDir):
            if os.path.isfile(modelDir + subDir + '/model.tar.gz'):
                metricsExist = True
    #if not metricsExist:
    #    print(cmd)
    print(cmd)


def getModel(modelName):
    modelPath = 'mtp/logs/' + modelName + '/'
    if not os.path.isdir(modelPath):
        print("error, model not found: " + modelPath, file=sys.stderr)
        return ''
    for model in sorted(os.listdir(modelPath), reverse=True):
        if os.path.isfile(modelPath + model + '/metrics.json'):
            modelPath = modelPath + model
            break
    if modelPath == 'mtp/logs/' + modelName + '/':
        print("error, model not found: " + modelPath, file=sys.stderr)
        return ''
    return modelPath[4:] + '/model.tar.gz'

def fixSingle(train, embeds, setting, dev):
    predDir = 'predictions/' + train + '/'

    predFile = predDir + setting + '.' + embeds + '.' + dev
    if not os.path.isfile(predFile):
        return
    newData = []
    for line in open(predFile):
        tok = line.strip().split('\t')
        if len(tok) > 2:
            tok[-1] = 'O'
        newData.append('\t'.join(tok) + '\n')
    outFile = open(predFile, 'w')
    for line in newData:
        outFile.write(line)
    outFile.close()

def getBoundaryPred(train, dev):
    if train == 'deda':
        predFile = 'predictions/boundaryawareNER/dade'
    else:
        predFile = 'predictions/boundaryawareNER/' + train

    if dev == 'german':
        predFile += '_NER-de-dev.noComments.tsv'
    elif dev == 'news':
        predFile += '_da_nosta-d-dev.tsv'
    elif dev == 'reddit':
        predFile += '_da_nosta-d-reddit-dev.tsv'
    elif dev == 'twitter':
        predFile += '_da_nosta-d-twitter-dev.tsv'
    elif dev == 'arto':
        predFile += '_da_nosta-d-arto-dev.tsv'
    else:
        predFile = '' 
    return predFile

def getScoreForSetting(train, embeds, setting, dev):
    allScores = []
    for seed in seeds:
        predDir = 'predictions/' + train + '/' 
        predFile = predDir + setting + '.' + embeds + '.' + dev + '.' + seed
        if setting == 'boundaryAware':
            predFile = getBoundaryPred(train, dev)
        if not os.path.isfile(predFile):
            print("NOT A FILE", predFile)
            return 0.0, 0.0

        goldPath = getDevFile(dev, setting)
        if 'goldNorm' in dev:
            goldPath = goldPath.replace('.tsv', '_goldNorm.tsv')
        if 'predNorm' in dev:
            goldPath = goldPath.replace('.tsv', '_predNorm.tsv')
     
        goldPath = goldPath.replace('_mh','')
        result = eval.eval(goldPath, predFile, False)
        allScores.append(result)
    return sum(allScores)/len(allScores), statistics.stdev(allScores)


