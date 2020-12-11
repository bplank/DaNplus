
def validate_post(post):
    try:
        anno_l1 = post['Layer1'].split(' ')
        anno_l2 = post['Layer2'].split(' ')
        text = post['text']
    except KeyError:
        return False, 4

    if len(anno_l1) != len(anno_l2):
        return False, 0
    elif '[removed]' in text:
        return False, 3
    elif len(text) != len(anno_l1):
        return False, 1
    else:
        return True, 2