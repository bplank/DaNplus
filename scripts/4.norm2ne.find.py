import sys

if len(sys.argv) < 3:
    print('please provide ne and norm file')
    exit(1)

def levenshtein(seq1, seq2):
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]

def readData(path):
    data = {}
    curSent = ''
    fullData = []
    for line in open(path):
        tok = line[:-1].split('\t')
        if len(line.strip()) < 1:
            data[curSent] = fullData
            curSent = ''
            fullData = []
        else:
            curSent += tok[0] + ' '
            if len(tok) == 1:
                tok.append('')
            fullData.append(tok)
    if fullData != []:
        data[curSent] = fullData
    return data

neData = readData(sys.argv[1])
normData = readData(sys.argv[2])

for sent in neData:
    #if sent not in normData:
    #    print(sent)
    #continue
    for tokNe, tokNorm in zip(neData[sent], normData[sent]):
        if ' ' in tokNorm[1]:
            for wordIdx, word in enumerate(tokNorm[1].split(' ')):
                ann = tokNe[1]
                if wordIdx > 0 and ann[0] == 'B':
                    ann = 'I' + ann[1:]
                print(word + '\t' + ann + '\t' + 'O')
        else:
            if tokNe[1] == '':
                tokNe[1] = 'O'
            if len(tokNe) == 1:
                tokNe.append('O')
            if len(tokNe) == 2:
                tokNe.append('O')
            if tokNorm[1] != '':
                print(tokNorm[1] + '\t' + tokNe[1] + '\t' + tokNe[2])
        #print(tokNorm[0] + '\t' + Norm[1])
    print()
        


