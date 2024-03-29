import unicodedata

from word2word import Word2word

de2en = Word2word('de', 'en')
fr2en = Word2word('fr', 'en')
ca2en = Word2word('ca', 'en')
it2en = Word2word('it', 'en')
es2en = Word2word('es', 'en')
ru2en = Word2word('ru', 'en')
pl2en = Word2word('pl', 'en')
bn2en = Word2word('bn', 'en')
# cy2en = Word2word('cy', 'en') - Not supported by word2word
da2en = Word2word('da', 'en')

en2de = Word2word('en', 'de')
en2fr = Word2word('en', 'fr')
en2ca = Word2word('en', 'ca')
en2it = Word2word('en', 'it')
en2es = Word2word('en', 'es')
en2ru = Word2word('en', 'ru')
en2pl = Word2word('en', 'pl')
en2bn = Word2word('en', 'bn')
# en2cy = Word2word('en', 'cy') - Not supported by word2word
en2da = Word2word('en', 'da')

source_map = {
    'de': de2en,
    'fr': fr2en,
    'ca': ca2en,
    'it': it2en,
    'es': es2en,
    'ru': ru2en,
    'pl': pl2en,
    'bn': bn2en,
    'da': da2en,
}

target_map = {
    'de': en2de,
    'fr': en2fr,
    'ca': en2ca,
    'it': en2it,
    'es': en2es,
    'ru': en2ru,
    'pl': en2pl,
    'bn': en2bn,
    'da': en2da,
}

supported_languages = list(source_map.keys())

stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves",
                "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
                "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
                "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
                "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above",
                "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
                "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                "only", "own", "same", "so", "than", "too", "very", "can", "will", "just", "don", "should", "now"]


class TranslationException(Exception):
    pass


def main():
    # word_translate('de', 'es', 'Baum')
    # text_translate('de', 'es', 'Das ist ein Baum'.split(' '))
    print(multilang_text_translate('de', 'stellenleitertagung in düsseldorf'.split(' ')))


def get_supported_languages():
    return supported_languages + ['en']


def multilang_text_translate(source, words: [str]):
    """
    Dictionary translate a list of words from source language to all other supported languages

    :param source: The source language
    :param words: Words to be translated
    :return: Best translation options in all target languages, or the original text if no translation was found
    """
    translations = [
        {"languageCode": source, "content": words}
    ]
    english_words = []
    english_words_filtered = []
    for word in words:
        try:
            translated_word = to_english(source, word)
            english_words.append(translated_word)
            if translated_word not in stopwords:
                # filter out stopwords before translating into other languages
                english_words_filtered.append(translated_word)
        except TranslationException:
            # do not further translate words, that have no english translation
            english_words_filtered.append('')
    if source == 'en':
        translations[0]['content'] = english_words_filtered
        translations[0]['contentOrig'] = english_words
    else:
        translations.append(
            {"languageCode": 'en', "content": english_words_filtered, "contentOrig": english_words}
        )

    for language in [language for language in supported_languages if language != source]:
        translations.append(
            {"languageCode": language, "content": text_translate('en', language, english_words_filtered)}
        )

    return translations


def text_translate(source, target, words: [str]):
    """
    Dictionary translate a list of words from source to target language

    :param source: The source language
    :param target: The target language
    :param words: Words to be translated
    :return: Best translation options in the target language, or the original text if no translation was found
    """
    return [word_translate(source, target, word) for word in words]


def word_translate(source, target, word):
    """
    Dictionary translate the given word from source to target language

    :param source: The source language
    :param target: The target language
    :param word: Single word for translation
    :return: Best translation option in the target language, or the original word if no translation was found
    """

    english_translation = to_english(source, word)

    final_translation = to_target(target, english_translation)

    return final_translation


def to_english(source, word):
    if source == 'en' or source == 'un':
        translations = [word]
    else:
        try:
            translations = source_map[source](word)
        except KeyError:
            # Fired when source language is non-existent,
            # or there is no translation for the word
            raise TranslationException

    print(f"Intermediate translation for '{word}' from {source} to en: {translations}")
    translation = get_first_valid_translation(translations, word)
    print(f'Picking best option {translation}')

    return translation


def to_target(target, word):
    try:
        translations = target_map[target](word)
    except KeyError:
        translations = [word]
    print(f"Translation for '{word}' from en to {target}: {translations}")
    translation = get_first_valid_translation(translations, word)
    print(f'Picking best option {translation}')
    return translation


def get_first_valid_translation(translation_list, fallback_word):
    for term in translation_list:
        if only_letters(term):
            return term
    return fallback_word


def only_letters(s):
    for c in s:
        cat = unicodedata.category(c)
        if cat not in ('Ll', 'Lu', 'Lo', 'Mc', 'Mn'):
            return False
    return True


def get_translated_terms(translations, language, unfiltered=True):
    for translation in translations:
        if translation['languageCode'] == language:
            if unfiltered:
                return translation['contentOrig']
            else:
                return translation['content']


if __name__ == '__main__':
    main()
