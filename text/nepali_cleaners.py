"""
Text cleaning and normalization for Nepali text.
"""
import re
import unicodedata

# -------------------- Helper Functions --------------------
def normalize_unicode(text):
    """Normalize text to NFC Unicode form."""
    return unicodedata.normalize('NFC', text)

def clean_symbols(text):
    """
    Keep only Devanagari letters, digits, basic punctuation, and whitespace.
    Removes any other unwanted symbols.
    """
    # Keep Devanagari range (U+0900 to U+097F), digits, and basic punctuation
    text = re.sub(r'[^ऀ-ॿ0-9.,?! ]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def expand_numbers(text):
    """
    Convert digits to Nepali words.
    Simple implementation - you can expand this as needed.
    """
    nepali_digits = {
        '0': 'शून्य', '1': 'एक', '2': 'दुई', '3': 'तीन', '4': 'चार',
        '5': 'पाँच', '6': 'छ', '7': 'सात', '8': 'आठ', '9': 'नौ',
        '०': 'शून्य', '१': 'एक', '२': 'दुई', '३': 'तीन', '४': 'चार',
        '५': 'पाँच', '६': 'छ', '७': 'सात', '८': 'आठ', '९': 'नौ'
    }
    
    def replace_digit(match):
        digit = match.group()
        return nepali_digits.get(digit, digit)
    
    # Replace single digits only (you can expand for multi-digit numbers)
    text = re.sub(r'[०-९0-9]', replace_digit, text)
    return text

# -------------------- Main Cleaner --------------------
def nepali_cleaners(text):
    """
    Complete text preprocessing pipeline for Nepali:
    1. Unicode normalization
    2. Clean symbols and punctuation
    3. Optionally expand numbers (commented out by default)
    """
    # Handle non-string inputs
    if isinstance(text, list):
        text = ' '.join(str(item) for item in text)
    if not isinstance(text, str):
        text = str(text)
    
    text = normalize_unicode(text)
    # text = expand_numbers(text)  # Uncomment if you want number expansion
    text = clean_symbols(text)
    return text

def basic_cleaners(text):
    """
    Minimal cleaning - just normalize unicode and clean whitespace.
    Use this if your text is already preprocessed into phonemes.
    """
    if isinstance(text, list):
        text = ' '.join(str(item) for item in text)
    if not isinstance(text, str):
        text = str(text)
    
    text = normalize_unicode(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()