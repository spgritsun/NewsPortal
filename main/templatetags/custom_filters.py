from django import template

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError("Фильтр цензурирования применяется только к строкам!")
    censored_words_given = ["скотина", "Мразь", "сволочь", "Идиот", "ублюдок", "редиска"]  # список слов для цензуры
    censored_words_lower = [word.lower() for word in censored_words_given]
    censored_words_capitalize = [word.capitalize() for word in censored_words_lower]
    censored_words = censored_words_lower + censored_words_capitalize
    for word in censored_words:
        if word in text:
            text = text.replace(word, word[0] + "*" * len(word[1:]))
    return text
