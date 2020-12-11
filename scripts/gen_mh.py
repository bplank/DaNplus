import os
COL_SEPARATOR = "\t"
MULTI_SEPARATOR = "$"
for neFile in os.listdir('data/'):
    neFile = 'data/' + neFile
    out_filename = neFile.replace('.tsv', "_mh.tsv")
    if os.path.isfile(out_filename) or '_mh' in neFile or os.path.isdir(neFile):
        continue
    out_f = open(out_filename, "w")
    with open(neFile, "r") as in_f:
        for line in in_f:
            if len(line) > 2:
                token_attrs = line.rstrip().split(COL_SEPARATOR)		
                if (token_attrs[1] == "O") and (token_attrs[2] == "O"):
                    new_label = "O"
                elif (token_attrs[1] != "O") and (token_attrs[2] == "O"):
                    new_label = token_attrs[1]
                elif (token_attrs[1] == "O") and (token_attrs[2] != "O"):
                    new_label = token_attrs[2]
                else:
                    labels = [token_attrs[1], token_attrs[2]]
                    labels.sort()
                    new_label = labels[0] + MULTI_SEPARATOR + labels[1]
                out_f.write(token_attrs[0] + COL_SEPARATOR + new_label + "\n")
            else:
                out_f.write(line)

    out_f.close()

