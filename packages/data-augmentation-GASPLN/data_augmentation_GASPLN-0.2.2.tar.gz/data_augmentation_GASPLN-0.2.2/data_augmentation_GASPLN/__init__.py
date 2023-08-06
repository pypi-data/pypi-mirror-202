import os
import pkg_resources
import random
import string
from typing import List, Tuple

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import spacy
import nltk
import translators as ts
import translators.server as tss
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Check if required NLTK resources are installed and download them if not.
nltk.download('punkt', 'corpora/stopwords', 'corpora/wordnet', 'taggers/averaged_perceptron_tagger')

# Load the synonyms_pt_BR.parquet file to a PyArrow table using pkg_resources to avoid hardcoding the path.
synonyms_table = pq.read_table(pkg_resources.resource_filename('data_augmentation_GASPLN', 'data/synonyms_pt_BR.parquet'))
synonyms_df = synonyms_table.to_pandas()

def synonyms_replacement(text: str, percentage: float = 0.25) -> str:
    """
    Replace a percentage of the words in the text with synonyms.
    
    Args:
    - text (str): The input text to be processed.
    - percentage (float): The percentage of words to be replaced with synonyms (default is 0.25).
    
    Returns:
    - str: The text with a percentage of words replaced with synonyms.
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
        
    return ''.join([' ' + token if not token.startswith("'") and token not in string.punctuation else token for token in tokens]).strip()

def back_translation(text: str, languages: List[str], translator: str) -> str:
    """
    Performs back translation of the given text, iterating over the provided languages in the list.

    Args:
    - text (str): The input text to be translated.
    - languages (List[str]): The list of languages to be used for back translation, excluding the original language.
                             The last language in the list must be Portuguese, unless it is the only language in the list.
    - translator (str): The name of the translator to be used for back translation. Must be one available at 
                        https://pypi.org/project/translators/#supported-translation-services

    Returns:
    - str: The back translated text.
    """
    # If the input text is empty, return an empty string
    if not text:
        return ""

    # If the list of languages is empty, return the original text
    if not languages:
        return text

    # Back translate the text for each language in the list, starting from the first language
    for lang in languages:
        text = ts.translate_text(query_text=text, to_language=lang, translator=translator)

    # If Portuguese is not the last language in the list, back translate to Portuguese as the last step
    if languages[-1] != 'pt':
        text = ts.translate_text(query_text=text, to_language='pt', translator=translator)

    return text

def character_swap(text: str, prob: float = 0.25) -> str:
    """
    Swaps characters in words of the input text with a given probability, except for words with less than or equal to 3 letters
    or for punctuation marks, keeping their positions in the word.
    
    Args:
    - text (str): The input text to swap characters in.
    - prob (float): The probability of swapping characters in each eligible word.
    
    Returns:
    - str: The text with characters swapped.
    """
    words = text.split()
    new_words = []
    
    for word in words:
        # Ignore words with less than or equal to 3 letters or with only punctuation marks
        if len(word) <= 3 or all(char in string.punctuation for char in word):
            new_words.append(word)
            continue
        
        # Randomly swap characters in the word with the given probability
        if random.random() < prob:
            word = word[0] + ''.join(random.sample(word[1:-1], len(word)-2)) + word[-1]
            
        new_words.append(word)
        
    return " ".join(new_words)


def random_swap(text: str, percentage: float = None, num_words: int = None, prob: float = 0.15) -> str:
    """
    Randomly swap words in a text. 
    
    Can specify either the percentage of words to swap, or the number of words to swap, or the probability of swapping 
    each word (with a default of 20%). 
    """
    words = text.split()
    
    # Calculate the number of words to swap based on the specified percentage or probability
    if percentage is not None:
        num_words = int(len(words) * percentage)
    elif prob is not None:
        num_words = 0
        for i in range(len(words) - 1):
            if random.random() < prob:
                num_words += 1
    
    # Swap the specified number of words randomly
    for _ in range(num_words):
        idx1, idx2 = random.sample(range(len(words)), 2)
        
        # Skip swapping if either word is a punctuation mark
        if not words[idx1].isalpha() or not words[idx2].isalpha():
            continue
            
        words[idx1], words[idx2] = words[idx2], words[idx1]
        
    return " ".join(words)

def add_noise(text: str, word_noise_prob: float = 0.2, char_noise_prob: float = 0.2) -> str:
    """
    Add noise to a percentage of the words in the text by inserting or removing letters.
    Additionally, swap punctuations with a small probability.
    """
    words = text.split()

    # Loop through each word
    for i, word in enumerate(words):
        # Determine if we add noise to the word
        if random.random() < word_noise_prob:
            # Determine if we add or remove letters
            if random.random() < char_noise_prob:
                # Add a random letter to the word
                random_letter = random.choice(string.ascii_lowercase)
                # Avoid adding a letter before a punctuation or after a whitespace
                if len(word) > 1 and not (word[0] in string.punctuation or word[-1].isspace()):
                    index = random.randint(1, len(word))
                    words[i] = word[:index] + random_letter + word[index:]
            else:
                # Remove a random letter from the word
                if len(word) > 2:
                    index = random.randint(1, len(word) - 2)
                    words[i] = word[:index] + word[index+1:]
        else:
            # Swap punctuations with a small probability
            if len(word) > 1 and random.random() < char_noise_prob:
                punct_indices = [i for i in range(len(word)) if word[i] in string.punctuation and i != 0 and i != len(word) - 1]
                if len(punct_indices) > 1:
                    idx1, idx2 = random.sample(punct_indices, 2)
                    words[i] = word[:idx1] + word[idx2] + word[idx1+1:idx2] + word[idx1] + word[idx2+1:]

        # Check that the word is still valid
        if len(words[i]) <= 1:
            continue

    return " ".join(words)

def text_augmentation(text: str, 
                      use_synonyms: bool = True, synonyms_percentage: float = 0.5,
                      use_back_translation: bool = False, languages: List[str] = ['en', 'es'], translator: str = 'google',
                      use_character_swap: bool = False, char_swap_prob: float = 0.25,
                      use_random_swap: bool = False, random_swap_percentage: float = None, num_words: int = None, random_swap_prob: float = 0.15,
                      use_add_noise: bool = True, word_noise_prob: float = 0.2, char_noise_prob: float = 0.2) -> str:
    """
    Apply multiple text augmentation techniques to the input text.
    """
    
    # Use synonyms to replace some words in the text
    if use_synonyms:
        text = synonyms_replacement(text, synonyms_df=synonyms_df, percentage=synonyms_percentage)
        
    # Use back translation to translate the text to a different language and back to the original
    if use_back_translation:
        text = back_translation(text, languages=languages, translator=translator)
        
    # Swap characters in the text
    if use_character_swap:
        text = character_swap(text, prob=char_swap_prob)
        
    # Swap random words in the text
    if use_random_swap:
        text = random_swap(text, percentage=random_swap_percentage, num_words=num_words, prob=random_swap_prob)
        
    # Add noise to the text
    if use_add_noise:
        text = add_noise(text, word_noise_prob=word_noise_prob, char_noise_prob=char_noise_prob)
        
    return text