import os
import eval
import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def getScores(sets, lang):
    trainSizes = []
    scores = []
    for i in range(17):
        iScores = []
        trainSizes.append((i+1) * 250)
        for devSet in sets:
            predFile = 'predictions/learningC/' + devSet + '.' + lang + '.' + str(i)
            print(predFile)
            if not os.path.isfile(predFile):
                break
            goldFile = 'data/da_' + devSet + '_dev.tsv'
            score = eval.eval(goldFile, predFile, False)
            iScores.append(score)
            print(goldFile, predFile, score)
        if len(iScores) != 0:
            scores.append(sum(iScores)/len(iScores))
    return trainSizes[:len(scores)], scores


fig, ax = plt.subplots(figsize=(8,5), dpi=300)
for training in ['deda', 'da']:
    for domains in [['news'], ['reddit', 'twitter', 'arto']]:
        x, scores = getScores(domains, training)

        print(x)
        print(scores)
        print()
        label = 'ID'
        if domains[0] != 'news':
            label = 'OOD'
        ax.plot(x, scores, label=training + '-' + label)

ax.set_xlabel('Number of sentences (train)')
ax.set_ylabel('Span-f1')
leg = ax.legend()
leg.get_frame().set_linewidth(1.5)

fig.savefig('learningC.pdf', bbox_inches='tight')





