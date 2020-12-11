import sys
import os
import json

useCache = False
cache = {}
if useCache and os.path.isfile('evalCache'):
    cache = json.load(open('evalCache')) 

def eval(goldPath, predPath, outerOnly=False):
    if useCache and predPath + '-' + goldPath in cache:
        return cache[predPath + '-' + goldPath]
    mergedFile = open('tmp.full', 'w')
    counter = 1
    for goldLine, predLine in zip(open(goldPath), open(predPath)):
        gold = goldLine.strip().split('\t')
        pred = predLine.strip().split('\t')
        if gold == ['']:
            mergedFile.write('\n')
        else:
            if len(pred) == 2:
                pred = [pred[0]] + pred[1].split('$')
            while len(pred) < 3:
                pred.append('O')
            while len(gold) < 3:
                gold.append('O')
            if outerOnly:
                gold[1] = 'O'
                pred[1] = 'O'
            if pred[-1] == '_':
                pred[-1] = 'O'
            mergedFile.write('\t'.join([str(counter)] + gold + pred[1:]) + '\n')
    mergedFile.close()
    cmd = 'perl scripts/nereval.perl < tmp.full > tmp.eval'
    os.system(cmd)
    score = 0.0
    for line in open('tmp.eval'):
        if line.startswith('FB1'):
            score = float(line.split(' ')[-1])
            break
    if useCache:
        cache[predPath + '-' + goldPath] = score
        json.dump(cache, open('evalCache', 'w'))
    return score

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please specify gold and predicted file')
        exit(1)
    useCache = False
    print(eval(sys.argv[1], sys.argv[2], False))
    print(eval(sys.argv[1], sys.argv[2], True))

