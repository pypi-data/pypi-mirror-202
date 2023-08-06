from googletrans import Translator
translator = Translator()

def to_uzbek(text):
    return translator.translate(text, dest='uz').text

def to_russian(text):
    return translator.translate(text, dest='ru').text

def to_english(text):
    return translator.translate(text, dest='en').text