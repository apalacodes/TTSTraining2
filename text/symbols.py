
_pad = "_"
_punctuation = "!,.? "
_special = "spn sil ८"
_devanagari_consonants = "क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह क्ष त्र ज्ञ"
_devanagari_vowels = "अ आ इ ई उ ऊ ऋ ॠ ए ऐ ओ औ"
_devanagari_matras = "ा ि ी ु ू ृ े ै ो ौ ं ः ँ"
_devanagari_other = "् ़"


# Combine all symbols - THIS IS THE FINAL LIST
symbols = (
    [_pad]
    + list(_punctuation)
    + _devanagari_consonants.split()
    + _devanagari_vowels.split()
    + _devanagari_matras.split()
    + _devanagari_other.split()
)