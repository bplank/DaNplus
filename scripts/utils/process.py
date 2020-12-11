import re
from tokenizer.tokenizer import RedditTokenizer

def process_text(text):
    REGEX_PATTERN = r"~[0-9]+(\.|,)?[0-9]*~|~|(&amp;#x200B;)" # Remove special cases like ~~45.65~~and &amp;#x220B

    patterns = {    ':Norway:':':regional_indicator_symbol_letter_n: :regional_indicator_symbol_letter_o:', 
                    ':Denmark:': ':regional_indicator_symbol_letter_d: :regional_indicator_symbol_letter_k:', 
                    ':man_facepalming_selector:': ':person_facepalming: ‍:male_sign:', 
                    ':woman_facepalming_selector:': ':person_facepalming: :female_sign:'
                }

    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text
    
    text = replace_all(text, patterns)
    text = re.sub(REGEX_PATTERN, '', text)
    return RedditTokenizer().tokenize(text)

def process_submissions(submission_generator, annotations):
    ids = [annotations[k]["ID"] for k in annotations.keys()]

    for submission in submission_generator:
        try:
            text = process_text(f'{submission.title}. {submission.selftext}')
            index = ids.index(submission.id)
            annotations[str(index)]["text"] = text
        except AttributeError:
            text = process_text(f'{submission.title}')
            index = ids.index(submission.id)
            annotations[str(index)]["text"] = text

    return annotations