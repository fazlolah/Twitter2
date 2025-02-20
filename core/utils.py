import re

def extract_hashtags(text):
    return set(re.findall(r'#(\w+)', text))