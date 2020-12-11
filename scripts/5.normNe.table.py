import eval
import myutils

def getNormScores(gold, pred):
    total = 0
    normed = 0
    cor = 0
    for goldLine, predLine in zip(open(gold), open(pred)):
        goldTok = goldLine.strip('\n').split('\t')
        predTok = predLine.strip('\n').split('\t')
        if goldTok == ['']:
            continue
        if len(goldTok) == 1:
            goldTok.append('')
        if goldTok[1] == predTok[0]:
            cor += 1
        if goldTok[0] != goldTok[1]:
            normed += 1
        total += 1
    base = (total-normed)/total
    acc = cor/total
    err = (acc - base)/(1-base)
    return base * 100, acc * 100, err * 100


translate = {'base': 'Baseline', 'pred': 'MoNoise', 'gold': 'Gold'}
for normStrat in ['base', 'pred', 'gold']:
    row = [translate[normStrat]]
    for task in ['norm', 'ne']:
        for dataset in ['twitter', 'arto']:
            if task == 'norm':
                goldPath = 'data/norm/' + dataset + '.norm'
                predPath = 'data/norm/' + dataset + '.norm.out'
                base, acc, err = getNormScores(goldPath, predPath)
                if normStrat == 'base':
                    row.append(base)
                if normStrat == 'pred':
                    row.append(acc)
                if normStrat == 'gold':
                    row.append(100.0)
            else:#NE
                neScores = []
                for seed in myutils.seeds:
                    normPart = ''
                    if normStrat != 'base':
                        normPart = '_' + normStrat + 'Norm'
                    goldPath = 'data/da_' + dataset + '_dev' + normPart + '.tsv'
                
                    normPart = ''
                    if normStrat != 'base':
                        normPart = '.' + normStrat + 'Norm'
                    predPath = 'predictions/deda/multi.ml.' + dataset + normPart + '.' + seed
                    neScores.append(eval.eval(goldPath, predPath, False))
                row.append(sum(neScores)/len(neScores))
    for i in range(1, len(row)):
        row[i] = '{:.2f}'.format(row[i])
    print( ' & '.join(row) + ' \\\\')


