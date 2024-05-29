import re
from collections import Counter
from spellchecker import SpellChecker

CUSTOM_LANGUAGE_DICTIONARY_MAP = {
    'jv': 'dictionary/javanese.txt',
    'id': 'dictionary/indonesian.txt',
    'kr': 'dictionary/korean.txt'
}

BUILTIN_LANGUAGES = {'en', 'es', 'fr', 'pt', 'de', 'it', 'ru', 'ar', 'eu', 'lv', 'nl'}

def load_words(dictionary_file):
    """Loads words from a given file and returns a Counter object."""
    with open(dictionary_file, 'r', encoding='utf-8') as file:
        text = file.read()
    return Counter(extract_words(text))

def extract_words(text):
    """Extracts words from text and returns them as a list."""
    return re.findall(r'\w+', text.lower())

def calculate_probability(word, word_counts, total_words):
    """Calculates the probability of `word`."""
    return word_counts[word] / total_words

def generate_candidates(word, word_counts):
    """Generates possible spelling corrections for the given word."""
    return (known([word], word_counts) or 
            known(edits1(word), word_counts) or 
            known(edits2(word), word_counts) or 
            [word])

def known(words, word_counts):
    """Returns the subset of words that appear in the dictionary."""
    return set(w for w in words if w in word_counts)

def edits1(word):
    """Returns all edits that are one edit away from the given word."""
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts    = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    """Returns all edits that are two edits away from the given word."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correct_word(word, word_counts, total_words):
    """Finds the most probable spelling correction for the given word."""
    candidates = generate_candidates(word, word_counts)
    return max(candidates, key=lambda w: calculate_probability(w, word_counts, total_words))

def correct_text_with_dictionary(paragraph, dictionary_file):
    """Corrects the spelling of words in a paragraph using a custom dictionary."""
    word_counts = load_words(dictionary_file)
    total_words = sum(word_counts.values())
    
    words_with_punctuation = re.findall(r'\b\w+\b|\S', paragraph)
    corrected_words = []
    
    for word in words_with_punctuation:
        if re.match(r'\w+', word):  # Only check words, skip punctuation
            corrected_word = correct_word(word, word_counts, total_words)
            corrected_words.append(corrected_word)

        else:
            corrected_words.append(word)
    
    corrected_paragraph = ''.join([
        f' {word}' if word not in '.,!?;:' else word
        for word in corrected_words
    ]).strip()
    
    return corrected_paragraph

def correct_text_with_language(paragraph, language):
    """Corrects the spelling of words in a paragraph using a specified language dictionary."""
    spell = SpellChecker(language=language)
    words_with_punctuation = re.findall(r'\b\w+\b|\S', paragraph)
    misspelled = spell.unknown(words_with_punctuation)
    
    corrected_words = []
    
    for word in words_with_punctuation:
        if word in misspelled:
            corrected_word = spell.correction(word)
            corrected_words.append(corrected_word)

        else:
            corrected_words.append(word)
    
    corrected_paragraph = ''.join([
        f' {word}' if word not in '.,!?;:' else word
        for word in corrected_words
    ]).strip()
    
    return corrected_paragraph

def correct_spelling(paragraph, language=None):
    """Corrects the spelling of words in a paragraph using a specified language dictionary."""
    if language:
        normalized_language = language.lower()

        if normalized_language in BUILTIN_LANGUAGES:
            return correct_text_with_language(paragraph, normalized_language)
        
        dictionary_file = CUSTOM_LANGUAGE_DICTIONARY_MAP.get(normalized_language)
        if dictionary_file:
            return correct_text_with_dictionary(paragraph, dictionary_file)
        else:
            raise ValueError(f"Unsupported language: {language}")
    else:
        raise ValueError("Language must be provided.")