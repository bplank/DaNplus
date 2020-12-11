
from psaw import PushshiftAPI
import os
import json

from utils.logs import write_logs
from utils.process import process_submissions
from utils.validate import validate_post


def create_annotation_file(annotations, filename):
    gen = PushshiftAPI().search_submissions(ids=[annotations[k]["ID"] for k in annotations.keys()], 
                                            subreddit='Denmark', 
                                            filter=['id', 'title', 'selftext', 'full_link', 'created_utc'])
    
    annotations = process_submissions(gen, annotations)
    
    with open(filename, 'w') as f, open('./logs.txt', 'a') as fp:
        for _, v in annotations.items():
            state, code = validate_post(v)
            if not state:
                print(f"\033[1;33;40m WARNING: \033[0m The submission {v['ID']} or annotations have changed since producing this data set. To learn more check the logs afterward (logs.txt)")
                write_logs(fp, v, code)
                continue
            try:
                for t, l1, l2 in zip(v['text'], v['Layer1'].split(' '), v['Layer2'].split(' ')):
                    f.write(f'{t}\t{l1}\t{l2}\n')
                f.write('\n')
            except KeyError:
                print(f"\033[1;33;40m WARNING:\033[0m Pulling the submission {v['ID']} produced an error leading to this KeyError. To learn more check the logs afterward (logs.txt)")
                write_logs(fp, v, 4)


def get_question2(answer):
    questions = []

    if answer['sets'] == 'Development':
        q = [{'type':'input', 'name':'dev_path', 'message': 'Please provide the path for the resulting development file'},
            {'type':'input', 'name':'dev_annotations', 'message': 'Please provide path for the annotations file for the development set', 'default':'../data/reddit/dev.json'}]
        questions.extend(q)
    elif answer['sets'] == 'Test':
        q = [{'type':'input', 'name':'test_path', 'message': 'Please provide the path for the resulting test file'},
            {'type':'input', 'name':'test_annotations', 'message': 'Please provide path for the annotations file for the test set', 'default':'../data/reddit/test.json'}]
        questions.extend(q)
    elif answer['sets'] == 'Both':
        q = [{'type':'input', 'name':'dev_path', 'message': 'Please provide the path for the resulting development file'},
            {'type':'input', 'name':'test_path', 'message': 'Please provide the path for the resulting test file'},
            {'type':'input', 'name':'dev_annotations', 'message': 'Please provide path for the annotations file for the development set', 'default':'../data/reddit/dev.json'},
            {'type':'input', 'name':'test_annotations', 'message': 'Please provide path for the annotations file for the test set', 'default':'../data/reddit/test.json'}]
        questions.extend(q)
    
    return questions


if __name__ == '__main__':
    # Build both Reddit development & test set using annotations and data fetched from pushift.io
    dev = json.load(open('./data/reddit_anno_dev.json'))
    create_annotation_file(dev, './data/da_reddit_dev.tsv')

    test = json.load(open('./data/reddit_anno_test.json'))
    create_annotation_file(test, './data/da_reddit_test.tsv')

