'''
PROGRAM DESCRIPTION:
Uses IBM AlchemyLanguage API to retrieve top keyword from input text.
Then finds most (conceptually) similiar word
    in 'word_list.txt'
'''

import json
from watson_developer_cloud import AlchemyLanguageV1
import editdistance
import os
import subprocess


# Credentials
URL = 'URL'
API_KEY = 'API_KEY'
alchemy_language = AlchemyLanguageV1(api_key=API_KEY)

# Get and clean user input
user_input = input('What would you like to say?: ').strip().lower()
user_input = "".join(c for c in user_input if c not in ('!','.',':','?'))

# Get keyword from API call
response = alchemy_language.combined(max_items = 1, text=user_input, extract=['keyword'])
keyword = response['keywords'][0]['text']
print('Keyword:',keyword)


# Prepare list of possible seed words
in_file = open('word_list.txt', 'r')
word_list = in_file.read().split()
word_list = [word.lower().strip('\'\"-,.:;!? ') for word in word_list]

# Find nearest word in our word_list
nearest = word_list[0]
for word in word_list:
    dist = editdistance.eval(keyword, word)
    if dist < editdistance.eval(keyword, nearest):
        nearest = word
print(nearest)      

# Pass 'nearest' into sample.py
subprocess.call("python sample.py --prime {}".format(nearest), shell=True)




