from pprint import pprint
import myutils
import os

def getTrainJson(train, embeds, setting):
    if train == 'da':
        trainFile = '../data/da_news_train.tsv'
        devFile = '../data/da_news_dev.tsv'
    elif train == 'de':
        trainFile = '../data/de_news_train.tsv'
        devFile = trainFile.replace('train', 'dev')
    elif train == 'deda':
        trainFile = '../data/dade_news_train.tsv'
        devFile = trainFile.replace('train', 'dev')

    if setting in ['single-merged', 'multilabel'] :
        trainFile = trainFile.replace('.tsv', '_mh.tsv')
        devFile = devFile.replace('.tsv', '_mh.tsv')


    name = '.'.join([train, embeds, setting])
    data = {'word_idx':0, 'tasks': {'ne1': {'column_idx':1, 'task_type': 'seq', 'metric':'span_f1'}}}
    data['train_data_path'] = trainFile
    data['validation_data_path'] = devFile

    if setting == 'multi':
        data['tasks']['ne2'] = {'column_idx':2, 'task_type': 'seq', 'metric':'span_f1'}
    if setting == 'multilabel':
        data['tasks']['ne1']['task_type'] =  'multiseq'
        data['tasks']['ne1']['metric'] =  'multi_span_f1'
        data['tasks']['ne1']['threshold'] = 0.9
    if setting == 'single-crf':
        data['tasks']['ne1']['task_type'] = 'masked_crf'
    return data


def run (train, embeds, setting, seed):
    datasets = {}
    datasets['DA'] = getTrainJson(train, embeds, setting)
    
    name = '.'.join([train, embeds, setting, seed])
    params = '../configs/params.' + embeds + '.' + seed + '.json'
    myutils.writeJson(datasets, name, params)
    
if not os.path.isdir('configs'):
    os.mkdir('configs')

for train in myutils.trains:
    for embed in myutils.embeds:
        for setting in myutils.settings:
            for seed in myutils.seeds:
                run(train, embed, setting, seed)

    
