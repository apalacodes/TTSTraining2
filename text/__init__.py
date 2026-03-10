""" from https://github.com/keithito/tacotron """
import re
from text import cleaners
from text.symbols import symbols

# Import Nepali cleaners
try:
    from text.nepali_cleaners import nepali_cleaners, basic_cleaners
except ImportError:
    print("Warning: nepali_cleaners not found, using default cleaners only")
    nepali_cleaners = None
    basic_cleaners = None

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")


def text_to_sequence(text, cleaner_names):
    """Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

    For Nepali: Text in curly braces like {क ् य ा} is treated as space-separated phonemes.
    For English: Text in curly braces is treated as ARPAbet.

    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through

    Returns:
      List of integers corresponding to the symbols in the text
    """
    sequence = []

    # Check for curly braces and treat their contents as phonemes/ARPAbet:
    while len(text):
        m = _curly_re.match(text)

        if not m:
            # No curly braces found, process normally
            sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
            break
        
        # Process text before curly braces
        sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
        
        # Process content inside curly braces as space-separated phonemes
        phoneme_text = m.group(2)
        sequence += _phoneme_to_sequence(phoneme_text, cleaner_names)
        
        # Continue with remaining text
        text = m.group(3)

    return sequence


def sequence_to_text(sequence):
    """Converts a sequence of IDs back to a string"""
    result = ""
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            result += s
    return result


def _clean_text(text, cleaner_names):
    """Apply text cleaners in sequence"""
    for name in cleaner_names:
        # First try to get from cleaners module
        cleaner = getattr(cleaners, name, None)
        
        # If not found, try Nepali cleaners
        if cleaner is None:
            if name == "nepali_cleaners" and nepali_cleaners:
                cleaner = nepali_cleaners
            elif name == "basic_cleaners" and basic_cleaners:
                cleaner = basic_cleaners
        
        if cleaner is None:
            raise Exception(f"Unknown cleaner: {name}")
        
        text = cleaner(text)
    
    return text


def _symbols_to_sequence(text):
    """Convert text to sequence of symbol IDs"""
    sequence = []
    
    # Handle space-separated phonemes
    if ' ' in text:
        symbols_list = text.split()
    else:
        # Single characters
        symbols_list = list(text)
    
    for s in symbols_list:
        if s in _symbol_to_id and _should_keep_symbol(s):
            sequence.append(_symbol_to_id[s])
        elif s.strip():  # Only warn for non-empty symbols
            print(f"Warning: Symbol '{s}' not found in vocabulary")
    
    return sequence


def _phoneme_to_sequence(text, cleaner_names):
    """
    Convert space-separated phonemes to sequence.
    Used for content inside curly braces like {क ् य ा न}
    """
    # Clean the phoneme text
    cleaned = _clean_text(text, cleaner_names)
    
    # Split by spaces to get individual phonemes
    phonemes = cleaned.split()
    
    sequence = []
    for phoneme in phonemes:
        if phoneme in _symbol_to_id:
            sequence.append(_symbol_to_id[phoneme])
        elif phoneme.strip():  # Only warn for non-empty phonemes
            print(f"Warning: Phoneme '{phoneme}' not found in vocabulary")
    
    return sequence


def _arpabet_to_sequence(text):
    """Legacy ARPAbet support (for English)"""
    return _symbols_to_sequence(["@" + s for s in text.split()])


def _should_keep_symbol(s):
    """Check if symbol should be kept in sequence"""
    return s in _symbol_to_id and s != "~"