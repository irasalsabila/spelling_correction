# Spelling Correction

## Overview

This Python project tackles the common frustration of typos, making it easier to ensure accurate and polished writing. Inspired by the need to address typos in my own writing, I've developed a tool that leverages Peter Norvig's algorithm. This not only corrects typos in English but also extends its capabilities to low-resource languages like Indonesian and Javanese.

The project consists of two core Python files: `spelling_correction_function.py` and `spelling_correction_api.py`. The `spelling_correction_function.py` file houses the core logic for typo correction, while `spelling_correction_api.py` provides a user-friendly API interface for easy integration into other applications.

## Features

- **Accurate Typo Correction**: The program identifies and corrects typos within sentences or paragraphs.
- **Multilingual Support**: The integrated dictionary supports various languages, including Indonesian, Javanese, English, Korean, and others from standard Python libraries.
- **Comprehensive Datasets**: For less-supported languages like Indonesian, the project leverages datasets from reliable sources like Kamus Besar Bahasa Indonesia (KBBI) and Indonesian articles. Javanese datasets include dictionaries and news and Wikipedia articles, while Korean utilizes news articles.

## Project Structure

```plaintext
Unscramble_Words/
├── README.md
├── spelling_correction_function.py
├── spelling_correction_api.py
├── .gitignore
├── requirements.txt
└── dictionary/
    ├── indonesian.txt
    ├── javanese.txt
    └── korean.txt
```
## Installation
To get started with the project, clone the repository and install the required dependencies.

```bash
git clone https://github.com/irasalsabila/spelling_correction.git
cd spelling_correction
pip install -r requirements.txt
```

## Usage
### Using the Functions Directly

You can use the functions provided in `spelling_correction_function.py` to unscramble words directly.

```python
import spelling_correction_function as sf

paragraph = "This is a sampple paragraph with somee missspelled words. It is meant to demonstrate how to check speling in a sentence."
language = 'en'

corrected_paragraph = sf.correct_spelling(paragraph, language=language)

print("\nOriginal paragraph:")
print(paragraph)
print("\nCorrected paragraph:")
print(corrected_paragraph)
```

### Using the API
The `spelling_correction_api.py` file provides an API interface for easier usage.

1. Time to predict using `127.0.0.1:5002/predict`
```json
{
    "text":"분석우: 전쟁 발발 이후 최악의 위기 상황에 처한 우크라이나나, 안녕하세요요요",
    "lang":"kr"
}
```

## Datasets
For less-supported languages like Indonesian, the project leverages datasets from reliable sources like Kamus Besar Bahasa Indonesia (KBBI) and Indonesian articles. Javanese datasets include dictionaries and news and Wikipedia articles, while Korean utilizes news articles.

## Contact
For any questions or suggestions, feel free to contact me at [irasalsabila@gmail.com].