import spacy
import nltk
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import translators as ts
import translators.server as tss
import pkg_resources
import random
import string

# check if punkt is installed, if not, install it
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
# check if stopwords is installed, if not, install it
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
# check if wordnet is installed, if not, install it
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    
# check if averaged_perceptron_tagger is installed, if not, install it
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
    
# load the synonyms_pt_BR.parquet file to a dataframe using pkg_resources to avoid hardcoding the path
synonyms_df = pd.read_parquet(pkg_resources.resource_filename('data_augmentation_GASPLN', 'data/synonyms_pt_BR.parquet'))

def synonyms_replacement(text, percentage=0.5):
    """
    Replace a percentage of the words in the text with synonyms.
    """
    
    tokens = nltk.word_tokenize(text)
    nlp = spacy.load('pt_core_news_sm')
    
    number_of_words = int(len(tokens) * percentage)
    indexes = np.random.choice(len(tokens), number_of_words, replace=False)
    
    for index in indexes:
        word = tokens[index]
        
        if len(word) == 1:
            continue
        
        syn_category = None
        for syn in synonyms_df.itertuples():
            if syn.word == word:
                syn_category = nlp(syn.synonyms[0])[0].pos_
                break
        
        if syn_category is None:
            continue
        
        word_category = nlp(word)[0].pos_
        
        if word_category != syn_category:
            continue
        
        synonyms = list(synonyms_df[synonyms_df['word'] == word]['synonyms'].values[0])
        
        if len(synonyms) == 0:
            continue
        
        synonym_index = np.random.randint(0, len(synonyms))
        tokens[index] = synonyms[synonym_index]
        
    return ' '.join(tokens)

def back_translation(sentence, languages=['en', 'es', 'pt'], translator='google'):
    """
    Translate the sentence to the next language in the list, using the specified translator, and then translate it back to the original language.
    """
        
    # Check if the sentence is a string
    if not isinstance(sentence, str):
        raise ValueError('Sentence must be a string')
    
    # Check if the sentence is not empty
    if sentence == '':
        raise ValueError('Sentence must not be empty')
    
    # For the number of languages, translate the sentence to the next language using the specified translator (if the last language is not pt, add it as the last language)
    for i in range(len(languages) - 1):
        sentence = ts.translate_text(query_text=sentence, to_language=languages[i + 1], translator=translator)
        
    # If the last language is not pt, translate the sentence to pt
    if languages[-1] != 'pt':
        sentence = ts.translate_text(query_text=sentence, to_language='pt', translator=translator)

    return sentence

def character_swap(sentence, p=0.25):
    """
    Swap two adjacent characters in the string with probability p.
    """
    words = sentence.split()
    for i in range(len(words)):
        if random.random() < p:
            word = words[i]
            if len(word) > 1:
                index = random.randint(0, len(word)-2)
                word = word[:index] + word[index+1] + word[index] + word[index+2:]
                words[i] = word
    return ' '.join(words)

def random_swap(text, num_swaps=None, percent_swaps=None):
    """
    Perform a random number or percentage of swaps of adjacent words in the input text.
    """
    words = text.split()
    num_words = len(words)
    
    # Calculate the number of swaps based on the input parameters
    if num_swaps is not None:
        num_swaps = min(num_swaps, num_words-1)
    elif percent_swaps is not None:
        num_swaps = int(num_words * percent_swaps)
    
    # Perform the swaps
    for _ in range(num_swaps):
        # Choose a random index i such that 0 <= i < len(words)-1
        i = random.randint(0, len(words)-2)
        # Swap the words at indices i and i+1
        words[i], words[i+1] = words[i+1], words[i]
    
    return ' '.join(words)

def random_deletion(sentence, p=0.1):
    """
    Perform random deletion of words in the input sentence with probability p.
    """
    words = sentence.split()
    remaining_words = [word for word in words if random.uniform(0, 1) > p]
    if len(remaining_words) == 0:
        return random.choice(words)
    else:
        return ' '.join(remaining_words)
    
def add_noise(text, word_p=0.25, char_p=0.1):
    """
    Add noise to the input text by randomly inserting or deleting characters in each word and
    by randomly deleting words with probabilities word_p and char_p, respectively.
    """
    words = text.split()
    new_words = []
    for word in words:
        if random.uniform(0, 1) < word_p:
            # With probability word_p, add noise to the word
            new_word = ""
            for char in word:
                if random.uniform(0, 1) < char_p:
                    # With probability char_p, delete the character
                    continue
                elif random.uniform(0, 1) < char_p:
                    # With probability char_p, insert a random character
                    new_word += random.choice(string.printable)
                new_word += char
            new_words.append(new_word)
        else:
            # Otherwise, keep the original word
            new_words.append(word)
    return ' '.join(new_words)

# Test add noise
print(add_noise('This is a test sentence'))