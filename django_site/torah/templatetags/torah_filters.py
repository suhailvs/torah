from django import template
register = template.Library()

PATTERN = 'abgdefzhjiklmnxopsqrct'

fiej = lambda p: p.replace('f','v').replace('i','y').replace('e','H').replace('j','T')

@register.filter(name='get_letternumber')
def get_letternumber(letter):
    """
    Return Number curresponding to PaleoHebrew letter
    """
    return PATTERN.index(letter)+1

@register.filter(name='get_words')
def get_words(line):
    """
    Return list of words of given line
    """
    return line.split(' ')

@register.filter(name='get_hebrewletter')
def get_hebrewletter(paleoletter):
    """
    Return Hebrew Letter curresponding to PaleoHebrew letter
    input: a
    output: \u05d0
    """
    HEBREW_UNICODE = ['\u05d0','\u05d1','\u05d2','\u05d3','\u05d4','\u05d5','\u05d6','\u05d7','\u05d8','\u05d9','\u05db','\u05dc','\u05de','\u05e0','\u05e1','\u05e2','\u05e4','\u05e6','\u05e7','\u05e8','\u05e9','\u05ea']
    return HEBREW_UNICODE[PATTERN.index(paleoletter)]

@register.filter(name='get_michigan_clairmont')
def get_michigan_clairmont(p):
    import re
    r={'e':'h','f':'w','h':'x','j':'+','i':'y','x':'s','s':'c','c':'$'}
    mc = re.sub(r'|'.join(r.keys()), lambda match: r[match.group(0)], p)
    return mc.upper()


@register.filter(name='replace_fie')
def replace_fie(paleoword):
    """
    Replace f -> v, i -> y, e -> H
    """
    return fiej(paleoword)


from torah.models import Word

@register.filter(name='get_englishword')
def get_englishword(paleoword):
    """
    Return English meaning curresponding to PaleoHebrew Word
    """
    w = Word.objects.get(name = paleoword[::-1])
    return w.translation