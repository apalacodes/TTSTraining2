import re
import unicodedata
from digits_to_word_nepali import digit_to_nepali_words  # you need to implement this

# -------------------- Helper Functions --------------------
def normalize_unicode(text):
    """Normalize text to NFC Unicode form."""
    return unicodedata.normalize('NFC', text)

def clean_symbols(text):
    """
    Keep only Devanagari letters, digits, basic punctuation, and whitespace.
    Removes any other unwanted symbols.
    """
    text = re.sub(r'[^ऀ-ॿ0-9.,?! ]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def expand_numbers(text):
    """
    Convert Devanagari digits or Arabic digits to Nepali words using `digit_to_nepali_words`.
    """
    dev_to_int = {
        '०':'0','१':'1','२':'2','३':'3','४':'4',
        '५':'5','६':'6','७':'7','८':'8','९':'9'
    }

    def replace_match(match):
        m = match.group()
        try:
            # Convert Devanagari digits to int
            arabic_num = ''.join(dev_to_int.get(c, c) for c in m)
            return digit_to_nepali_words(int(arabic_num))
        except:
            return m

    return re.sub(r'[०-९0-9]+', replace_match, text)

# -------------------- Main Cleaner --------------------
def nepali_cleaners(text):
    """
    Complete text preprocessing pipeline for Nepali:
    1. Unicode normalization
    2. Number expansion to Nepali words
    3. Clean symbols and punctuation
    """
    # Handle non-string inputs
    if isinstance(text, list):
        text = ' '.join(str(item) for item in text)
    if not isinstance(text, str):
        text = str(text)

    text = normalize_unicode(text)
    text = expand_numbers(text)
    text = clean_symbols(text)
    return text