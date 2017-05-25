from math import sqrt, exp, pi

def frange(start, stop, step=.1):
    x = start
    while x < stop:
        yield float('{0:.2f}'.format(x))
        x += step


def style_to_int(style: str):
    assert style and type(style) == str
    style = style.upper()
    if style == 'CONVERGENTE':
        return 0
    elif style == 'DIVERGENTE':
        return 1
    elif style == 'ACOMODADOR':
        return 2
    elif style == 'ASIMILADOR':
        return 3
    else:
        raise ValueError('{} is not a valid style.'.format(style))


def gender_full_text(g: str):
    g = g.upper()
    if g == 'M':
        gender = 'Masculino'
    elif g == 'F':
        gender = 'Femenino'
    else:
        raise ValueError('{} is not a valid gender value'.format(g))

    return gender


def nothing(x): x
