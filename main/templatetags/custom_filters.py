from django import template

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError("Фильтр цензурирования применяется только к строкам!")
    censored_words = ["Скотина", "скотина", "Мразь", "мразь", "Сволочь", "сволочь", "Идиот", "идиот",
                      "Ублюдок", "ублюдок", "Редиска", "редиска"]  # список слов для цензуры
    for word in censored_words:
        if word.upper() in text.upper():
            text = text.replace(word, word[0] + "*" * len(word[1:]))
    return text
