import sys

if len(sys.argv) < 5:
    print('please provide input file, 2 output files and splitPoint')
    exit(1)


def readData(path):
    data = []
    fullData = []
    for line in open(path):
        if len(line.strip()) < 1:
            data.append(fullData)
            fullData = []
        else:
            fullData.append(line[:-1])
    return data

data = readData(sys.argv[1])

split = int(sys.argv[4])

out1 = open(sys.argv[2], 'w')
for sent in data[:split]:
    out1.write('\n'.join(sent) + '\n\n')

out2 = open(sys.argv[3], 'w')
for sent in data[split:]:
    out2.write('\n'.join(sent) + '\n\n')

out1.close()
out2.close()
