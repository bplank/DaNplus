import eval
import os
import myutils

table = ''
for norm in [False, True]:
    for embed in ['ml', 'da']:
        scores = []
        for test in myutils.devs:
            seedScores = []
            for seed in myutils.seeds:
                predFile = 'predictions/test/test.' + test + '.' + embed + '.' + seed
                goldFile = myutils.getTestFile(test, 'multi')
                if norm:
                    predFile = predFile[:-2] + '.predNorm' + predFile[-2:]
                    goldFile = goldFile.replace('.tsv', '_predNorm.tsv')
                if not os.path.isfile(predFile):
                    seedScores.append(0)
                else:
                    seedScore = eval.eval(goldFile, predFile, False)
                    seedScores.append(seedScore)
                print(predFile, seedScores[-1])
            avgScore = '{:.2f}'.format(sum(seedScores)/len(seedScores))
            if avgScore == 0.0:
                scores.append('---')
            else:
                scores.append(avgScore)
        name = embed + ('-predNorm' if norm else '')
        table += ' & '.join([name] + scores) + ' \\\\\n'
print(' & '.join(myutils.devs))
print(table)
