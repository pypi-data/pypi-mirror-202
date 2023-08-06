# Data Augmentation Library for Portuguese (Brazil)

This is a research project developed in collaboration with the [GASPLN](https://wp.ufpel.edu.br/gaspln/) research group of the Federal University of Pelotas (UFPel) aimed at creating a Python library for Data Augmentation in Portuguese (Brazil).

## Table of Contents
- [Installation](#installation)  
- [Usage](#usage)
    - [Synonym Replacement](#synonym-replacement)
    - [Back Translation](#back-translation)
    - [Character Swap](#character-swap)
    - [Random Swap](#random-swap)
    - [Random Deletion](#random-deletion)
    - [Add Noise](#add-noise)


## Installation

The package is available on PyPI and can be easily installed using pip:

```bash
pip install data_augmentation_GASPLN
```

You also need to download the Portuguese model for spaCy. To do this, run the following command:

```bash
python -m spacy download pt_core_news_sm
```

## Usage

***PLEASE NOTE THAT THIS PROJECT IS STILL UNDER CONSTRUCTION AND NOT YET READY FOR USE***

That being said, the library currently has some test functions that can be used, as shown below.

To use the library, simply import it as follows:

```python
from data_augmentation_GASPLN import data_augmentation as da
```

### Synonym Replacement

The `synonyms_replacement()` function can be used for synonym replacement. Here's an example:

```python
da.synonyms_replacement("Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes de alguma forma a fim de criar novos dados.", 0.5)
```

The first parameter is the text to be augmented, and the second parameter is the percentage of words to be replaced by synonyms (by default, and in this example, 50% of the words in the text).

### Back Translation

The `back_translation()` function can be used for back translation. Here's an example:

```python
da.back_translation('Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes em conjuntos de dados de treinamento.', languages=['en', 'es', 'ru'], translator='google')
```

- The `first parameter` is the text to be augmented;
- The `second parameter` is a list of languages to be used for back translation (by default it translates to English, Spanish and back to Portuguese*)
    * It is not necessary to include Portuguese in the list of languages, as the text will be translated to Portuguese at the end of the process;
- The `third parameter` is the translator to be used (by default it uses Google Translate).

A list of the available languages and translators can be found [here](https://pypi.org/project/translators/#supported-languages).

### Character Swap

The `character_swap()` function performs  random character swaps in the text. Here's an example:

```python
da.character_swap("Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes de alguma forma a fim de criar novos dados.", 0.25)
```

- The `first parameter` is the text to be augmented;
- The `second parameter` is probability of two adjacent characters being swapped (by default, and in this example, 25%).

### Random Swap

The `random_swap()` performs a random number or percentage of swaps of adjacent words in the input text.

```python

da.random_swap("Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes de alguma forma a fim de criar novos dados.", num_swaps=2)
```

- The `first parameter` is the text to be augmented;
- The `second parameter` must be one of the following:
    - `num_swaps`: the number of swaps to be performed
    - `percent_swaps`: the percentage of words to be swapped.
    **NOTE**: Both parameters are mutually exclusive and are set to `None` by default.

### Random Deletion

The `random_deletion()` function performs random deletion of words in the input sentence with probability p.

```python
da.random_deletion("Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes de alguma forma a fim de criar novos dados.", p=0.1)
```

- The `first parameter` is the text to be augmented;
- The `second parameter` is the probability of a word being deleted (by default, and in this example, 10%).

### Add Noise

The `add_noise()` function adds noise to the input text by randomly inserting or deleting characters of the input text.

```python
da.add_noise("Data augmentation é uma técnica de aprendizado de máquina que aumenta o número de dados de treinamento, alterando os dados existentes de alguma forma a fim de criar novos dados.", word_p=0.25, char_p=0.1):
```

- The `first parameter` is the text to be augmented;
- The `second parameter` is the probability of a word to noise being added (by default, and in this example, 25%);
- The `third parameter` is the probability of noise being applied to a word selected for noise addition (by default, and in this example, 10%).
