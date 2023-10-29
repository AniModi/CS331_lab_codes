import csv

csv_file = 'mails.csv'

email_bodies = []
with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        email_bodies.append(row[2])  # The email body is in the third column


import random
from collections import defaultdict, Counter
from nltk.util import ngrams

# Create a trigram model
trigram_model = defaultdict(Counter)
bigram_model = defaultdict(Counter)

import re

for body in email_bodies:
    body = re.sub(r'[^a-zA-Z0-9.]', ' ', body)
    tokens = body.split()
    trigrams = list(ngrams(tokens, 3))
    bigrams = list(ngrams(tokens, 2))
    for trigram in trigrams:
        trigram_model[(trigram[0], trigram[1])][trigram[2]] += 1
    for bigram in bigrams:
        bigram_model[bigram[0]][bigram[1]] += 1

# Function to generate text
def generate_text(start, length=50):
    current_pair = start
    text = list(current_pair)
    for _ in range(length):
        next_word_candidates = trigram_model[current_pair]
        next_word = random.choices(
            list(next_word_candidates.keys()), 
            list(next_word_candidates.values())
        )[0]
        text.append(next_word)
        current_pair = (current_pair[1], next_word)
    return ' '.join(text)


def generate_text_2(start, length=50):
    current = start
    text = [current]
    for _ in range(length):
        next_word_candidates = bigram_model[current]
        next_word = random.choices(
            list(next_word_candidates.keys()), 
            list(next_word_candidates.values())
        )[0]
        text.append(next_word)
        current = next_word
    return ' '.join(text)

# Generate some text starting with a pair of words
print(generate_text_2(('Confused'), 30))
