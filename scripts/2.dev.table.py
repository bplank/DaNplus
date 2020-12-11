import os
import eval
import myutils

data = {}
for train in myutils.trains:
    for embed in myutils.embeds:
        for setting in myutils.settings:
            for dev in myutils.devs:
                if setting in ['single', 'single-crf']:
                    myUtils.fixSingle(train, embed, setting, dev)
                score, _ = myutils.getScoreForSetting(train, embed, setting, dev)
                trainName = train + '.' + embed + '.' + setting
                print(trainName, score, dev)
                if trainName not in data:
                    data[trainName] = {}
                data[trainName][dev] = score

tableData = []
for train in myutils.trains:
    for embed in myutils.embeds:
        for setting in myutils.settings: #+ ['boundaryAware']:
            trainName = train + '.' + embed + '.' + setting
            #if setting == 'boundaryAware':
            #    trainName = 'boundaryAware.' + train
            scores = [trainName]
            for devName in myutils.devs: 
                scores.append('{:.2f}'.format(data[trainName][devName]))
            tableData.append(scores)

for i in range(1,len(tableData[0])):
    scores = []
    for j in range(0,len(tableData)):
        scores.append(float(tableData[j][i]))
    for j in range(1,len(tableData)):
        if float(tableData[j][i]) == max(scores):
            tableData[j][i] = '\\textbf{' + tableData[j][i] + '}'

print(' & '.join([' '] + myutils.devs) + ' \\\\')
for row in tableData:
    print(' & '.join(row) + ' \\\\') 
            

