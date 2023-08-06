# Data Augmentation Library for Portuguese (Brazil)

This is a research project developed in collaboration with the [GASPLN](https://wp.ufpel.edu.br/gaspln/) research group of the Federal University of Pelotas (UFPel) aimed at creating a Python library for Data Augmentation in Portuguese (Brazil).

## Table of Contents
- [Installation](#installation)  
- [Usage](#usage)
    - [Synonym Replacement](#synonyms-replacement-function)
    - [Back Translation](#back-translation-function)
    - [Character Swap](#character-swap-function)
    - [Random Swap](#random-swap-function)
    - [Add Noise](#add-noise-function)
    - [Text Augmentation](#text-augmentation-function)


# Installation

The package is available on PyPI and can be easily installed using pip:

```bash
pip install data_augmentation_GASPLN
```

You also need to download the Portuguese model for spaCy. To do this, run the following command:

```bash
python -m spacy download pt_core_news_sm
```

# Usage

## Synonyms Replacement Function

This function is used to replace a percentage of words in a given text string with their synonyms. It takes three arguments: `text`, `synonyms_df`, and `percentage`.

### Arguments:

* `text` (str): The input text to be processed. This can be any string, but should ideally be a full sentence or paragraph for best results.

* `percentage` (float, optional): The percentage of words in the input `text` that should be replaced with their synonyms. The default value is 0.25, which means that 25% of the words in the input text will be replaced.

### Example Usage:

Here's an example of how to use the `synonyms_replacement` function:

```python
from data_augmentation_GASPLN import synonyms_replacement

# Call the function with the following parameters
text = "Texto a ser augmentado aqui."
augmented_text = synonyms_replacement(text, percentage=0.25)

# Print the result
print(augmented_text)
```

## Back Translation Function

This function performs back translation of the given text, iterating over the provided languages in the list. 

### Arguments:

* `text` (str): The input text to be translated. 
* `languages` (List[str]): The list of languages to be used for back translation, excluding the original language. The last language in the list must be Portuguese, unless it is the only language in the list (it will be automatically added if not provided).
* `translator` (str): The name of the translator to be used for back translation. Must be one available at https://pypi.org/project/translators/#supported-translation-services

### Example Usage:

```python
from data_augmentation_GASPLN import back_translation

# Call the function with the following parameters
text = "Text to be back translated here."
languages = ['es', 'fr', 'pt']
translator = 'google'

augmented_text = back_translation(text, languages, translator)

# Print the result
print(augmented_text)
```

## Character Swap Function

This function is used to swap characters in words of the input text with a given probability, except for words with less than or equal to 3 letters or for punctuation marks, keeping their positions in the word. It takes two arguments: `text` and `prob`.

### Arguments:

* `text` (str): The input text to swap characters in. This can be any string, but should ideally be a full sentence or paragraph for best results.

* `prob` (float, optional): The probability of swapping characters in each eligible word. The default value is 0.25, which means that there is a 25% chance of swapping characters in each eligible word.

### Example Usage:

Here's an example of how to use the `character_swap` function:

```python
from data_augmentation_GASPLN import character_swap

# Call the function with the following parameters
text = "Texto a ser augmentado aqui aqui."
augmented_text = character_swap(text, prob=0.4)

# Print the result
print(augmented_text)
```

## Random Swap Function

This function randomly swaps words in a text. You can specify either the percentage of words to swap, or the number of words to swap, or the probability of swapping each word (with a default of 20%).

### Arguments:

* `text` (str): The input text to swap words in. This can be any string.

* `percentage` (float, optional): The percentage of words to swap in the input text. The default value is None.

* `num_words` (int, optional): The number of words to swap in the input text. The default value is None.

* `prob` (float, optional): The probability of swapping each word in the input text. The default value is 0.15.

### Example Usage:

Here's an example of how to use the `random_swap` function:

```python
from data_augmentation_GASPLN import random_swap

# Call the function with the following parameters
text = "Texto a ser augmentado aqui."
augmented_text = random_swap(text, percentage=0.25)

# Print the result
print(augmented_text)
```

## Add Noise Function

This function is used to add noise to a percentage of the words in a given text string by inserting or removing letters, and swapping punctuations with a small probability. It takes three arguments: `text`, `word_noise_prob`, and `char_noise_prob`.

### Arguments:

* `text` (str): The input text to be processed. This can be any string, but should ideally be a full sentence or paragraph for best results.

* `word_noise_prob` (float, optional): The probability of adding noise to a given word. The default value is 0.2, which means that 20% of the words in the input text will have noise added to them.

* `char_noise_prob` (float, optional): The probability of adding or removing a letter from a given word. The default value is 0.2, which means that there is a 20% chance that a letter will be added or removed from a word.

### Example Usage:

Here's an example of how to use the `add_noise` function:

```python
from data_augmentation_GASPLN import add_noise

# Call the function with the following parameters
text = "Texto a ser augmentado aqui."
augmented_text = add_noise(text, word_noise_prob=0.2, char_noise_prob=0.2)

# Print the result
print(augmented_text)
```
## Text Augmentation Function

This function applies multiple text augmentation techniques to the input text. It takes several arguments that determine which techniques are used and with what parameters.

### Arguments:

* `text` (str): The input text to be processed.

* `use_synonyms` (bool, optional): Whether or not to use synonym replacement. Default is `True`.

* `synonyms_percentage` (float, optional): The percentage of words in the input text that should be replaced with their synonyms. Default is 0.5.

* `use_back_translation` (bool, optional): Whether or not to use back translation. Default is `False`.

* `languages` (List[str], optional): A list of two-letter language codes representing the languages to translate the text to and back from. Default is `['en', 'es']`.

* `translator` (str, optional): The name of the translator to use for back translation. Currently, the only supported value is `'google'`. Default is `'google'`.

* `use_character_swap` (bool, optional): Whether or not to use character swap. Default is `False`.

* `char_swap_prob` (float, optional): The probability of swapping a character in a word. Default is 0.25.

* `use_random_swap` (bool, optional): Whether or not to use random word swap. Default is `False`.

* `random_swap_percentage` (float, optional): The percentage of words in the input text to swap with other words. If `num_words` is specified, this parameter is ignored. Default is `None`.

* `num_words` (int, optional): The number of words to swap with other words in the input text. If `num_words` is specified, `random_swap_percentage` is ignored. Default is `None`.

* `random_swap_prob` (float, optional): The probability of swapping a word in the text. Default is 0.15.

* `use_add_noise` (bool, optional): Whether or not to add noise to the text. Default is `True`.

* `word_noise_prob` (float, optional): The probability of adding noise to a word in the text. Default is 0.2.

* `char_noise_prob` (float, optional): The probability of adding or removing a character in a word in the text. Default is 0.2.

### Example Usage:

Here's an example of how to use the `text_augmentation` function:

```python
from data_augmentation_GASPLN import text_augmentation

# Call the function with the following parameters
text = "Texto a ser augmentado aqui."
augmented_text = text_augmentation(text, 
                                    use_synonyms=True, synonyms_percentage=0.4, 
                                    use_back_translation=True, languages=['en', 'fr'], translator='google', 
                                    use_character_swap=True, char_swap_prob=0.3, 
                                    use_random_swap=True, num_words=2, random_swap_prob=0.2, 
                                    use_add_noise=True, word_noise_prob=0.3, char_noise_prob=0.3)

# Print the result
print(augmented_text)
```