import os

for normSetting in ['pred', 'gold']:
    for dataset, split in zip(['twitter', 'arto'], [119, 336]):
        normPrefix = '' if normSetting == 'gold' else '.out'
        normFile = 'data/norm/' + dataset + '.norm' + normPrefix
        devNorm = normFile + '.dev' + normPrefix
        testNorm = normFile + '.test' + normPrefix
        devNE = 'data/da_' + dataset + '_dev.tsv'
        testNE = 'data/da_' + dataset + '_test.tsv'
        devNEnorm = 'data/da_' + dataset + '_dev_' + normSetting + 'Norm.tsv'
        testNEnorm = 'data/da_' + dataset + '_test_' + normSetting + 'Norm.tsv'

        splitCmd = 'python3 scripts/3.norm2ne.split.py ' + normFile + ' ' + devNorm + ' ' + testNorm + ' ' + str(split)
        devCmd = 'python3 scripts/3.norm2ne.merge.py ' + devNE + ' ' + devNorm + ' > ' + devNEnorm
        testCmd = 'python3 scripts/3.norm2ne.merge.py ' + testNE + ' ' + testNorm + ' > ' + testNEnorm

        print(splitCmd)
        os.system(splitCmd)
        print(devCmd)
        os.system(devCmd)
        print(testCmd)
        os.system(testCmd)
