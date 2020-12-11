import os
import eval
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import myutils

# skip german to save space
devsToUse = myutils.devs[1:]

data = {}
for train in myutils.trains:
    for setting in myutils.settings:
        for dev in devsToUse:
            for embed in myutils.embeds:
                if setting == 'single':
                    myUtils.fixSingle(train, embed, setting, dev)
                score, stdev = myutils.getScoreForSetting(train, embed, setting, dev)
                settingName = setting + '.' + embed
                if settingName not in data:
                    data[settingName] = {}
                if train not in data[settingName]:
                    data[settingName][train] = {}
                data[settingName][train][dev] = (score, stdev)

fig, ax = plt.subplots(figsize=(15,4), dpi=300)
modelIdx = 0
colors = myutils.colors + myutils.colors
for setting in myutils.settings:
    for embed in myutils.embeds:
        settingName = setting + '.' + embed
        scores = []
        stdevs = []
        for dev in devsToUse:
            for train in myutils.trains:
                print(train, dev, setting, embed, data[settingName][train][dev][0], data[settingName][train][dev][1])
                scores.append(data[settingName][train][dev][0])
                stdevs.append(data[settingName][train][dev][1])
        barWidth = 1/(len(devsToUse)+3)
        idxs = []
        for i in range(len(scores)):
            idxs.append(i + barWidth * (modelIdx + 1))

        print(settingName)
        print(["{:.2f}".format(score) for score in scores])
        print(["{:.2f}".format(stdev) for stdev in stdevs])
        print()
        if setting == 'multi':
            settingName = 'multitask.' + embed
        if modelIdx%2 == 1:
            ax.bar(idxs, scores, barWidth, yerr=stdevs, label=settingName, color=colors[int(modelIdx/2)], edgecolor='black', hatch='//')
        else:
            ax.bar(idxs, scores, barWidth, yerr=stdevs, label=settingName, color=colors[int(modelIdx/2)], edgecolor='black')
        modelIdx += 1
        
labels = myutils.trains * len(devsToUse)
myutils.setTicks(ax, labels, 45)

ax.plot([3,3],[0,100], color='black')
ax.plot([6,6],[0,100], color='black')
ax.plot([9,9],[0,100], color='black')
plt.text(1, 7.5, devsToUse[0], fontsize=18)
plt.text(4, 7.5, devsToUse[1], fontsize=18)
plt.text(7, 7.5, devsToUse[2], fontsize=18)
plt.text(10, 7.5, devsToUse[3], fontsize=18)

ax.set_ylabel('Span F1')
ax.set_ylim((30,85))
ax.set_xlim((0,12))
leg = ax.legend(loc='upper right', ncol=3, bbox_to_anchor=(1, 1.025))
leg.get_frame().set_linewidth(1.5)

fig.savefig('fullResults.pdf', bbox_inches='tight')


