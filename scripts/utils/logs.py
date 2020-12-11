
def write_logs(fp, v, code):
    if code == 0:
        fp.write(f"{v['ID']}: Error in the annotations. The length of the two columns of annotations no longer match, thus producing this error. Layer 1 has length {len(v['Layer1'])} and Layer 2 has length {len(v['Layer2'])}. Something have changed in either the 'dev.json' or the 'test.json'.\n\n")
    elif code == 1:
        fp.write(f"{v['ID']}: Error in the data source. The length of the two columns of annotations and the length of text no longer match, thus producing this error. This is most likely due to a change in the source data from 'pushshift.io'. Please alert us on Github by opening an Issue with the id of the post throwing this error.\n\n")
        fp.write(f"{v['text']}, {len(v['text'])}\n\n")
    elif code == 3:
        fp.write(f"{v['ID']}: Error in the data source. The body of the original submission have been deleted since producing these annotations, thus rendering it unusable. This is due to a change in the source data from 'pushshift.io'. Please alert us on Github by opening an Issue with the id of the post throwing this error.\n\n")
    elif code == 4:
        fp.write(f"{v['ID']}: Pulling the submission created an error such that no text existed. This is most likely due to a deletion of said submission in the pushshift.io API. Please alert us on Github by opening an Issue with the id of the post throwing this error.\n\n")