for dataset in ['arto', 'twitter']:
    trainPath = '../../data/norm/' + dataset + '.norm'
    cmd = 'cd monoise/src/ && ./tmp/bin/binary -m KF -r ../working/' + dataset + ' -i ' + trainPath + ' -d ../data/da -C -f 111101111111 > ' + trainPath + '.out 2> ' + trainPath + '.err'
    print(cmd)



