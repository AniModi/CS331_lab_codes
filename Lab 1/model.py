import csv
import random
from collections import defaultdict, Counter
from nltk.util import ngrams
import re
import nltk

# Download the NLTK words corpus if you haven't already

# Load the English words set
english_words = set(nltk.corpus.words.words())

csv_file = 'mails.csv'

email_bodies = []
with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        email_bodies.append(row[2])  # The email body is in the third column

# Create a trigram model
trigram_model = defaultdict(Counter)
bigram_model = defaultdict(Counter)

for body in email_bodies:
    body = re.sub(r'[^a-zA-Z0-9.]', ' ', body)
    tokens = body.split()

    # Filter out non-English words
    english_tokens = [word for word in tokens if word.lower() in english_words]

    trigrams = list(ngrams(english_tokens, 3))
    bigrams = list(ngrams(english_tokens, 2))

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
print(generate_text_2(('Information'), 100))


# Print the Bigram Model
# Print a small subset of the bigram model
# print('|-------------------------Bigram Model (Sample)----------------------------------------|')
# for key, value in list(bigram_model.items())[:5]:
#     print(f"Bigram: {key}, Next Words: {list(value.keys())[:5]}")

# # Print a small subset of the trigram model
# print('|-------------------------Trigram Model (Sample)----------------------------------------|')
# for key, value in list(trigram_model.items())[:5]:
#     print(f"Trigram: {key}, Next Words: {list(value.keys())[:5]}")

