import sys

if len(sys.argv) < 3:
    print('please provide ne and norm file')
    exit(1)

for neLine, normLine in zip(open(sys.argv[1]), open(sys.argv[2])):
    neTok = neLine[:-1].split('\t')
    normTok = normLine[:-1].split('\t')
    if neLine.strip() == '':
        print()
    elif ' ' in normTok[-1]:
        for wordIdx, word in enumerate(normTok[-1].split(' ')):
            if wordIdx > 0 and neTok[1] != 'O':
                newTag = '\t'.join(neTok[1:])
                newTag = 'I' + newTag[1:]
                print(word + '\t' + newTag)
            else:
                print(word + '\t' + '\t'.join(neTok[1:]))
    elif normTok[-1] != '':
        print(normTok[-1] + '\t' + neTok[1] + '\t' + neTok[2])


