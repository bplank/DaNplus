import ast
from pprint import pprint

for training in ['deda', 'da']:
    config = ast.literal_eval(' '.join(open('configs/da.ml.multi.1.json').readlines()))
    if training == 'deda':
        config.update(ast.literal_eval(' '.join(open('configs/de.ml.multi.1.json').readlines())))
    for i in range(17):
        config['DA']['max_sents'] = (i+1) * 250
        configPath = 'configs/learningc.' + training + '.' + str(i) + '.json'
        pprint(config, open(configPath, 'wt'))
        cmd = 'cd mtp && python3 train.py --device 0 --dataset_config ../' 
        cmd += configPath + ' --name learningC.' + training + '.' + str(i) + ' --parameters_config ../configs/params.ml.1.json && cd ../'
        print(cmd)

