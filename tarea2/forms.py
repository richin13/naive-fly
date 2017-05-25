from flask_wtf import FlaskForm
from wtforms import IntegerField, HiddenField, SelectField, FloatField, ValidationError
from wtforms.validators import DataRequired
from .util import style_to_int

required = [DataRequired('Este campo es requerido'), ]


class StylesClassicForm(FlaskForm):
    ca_ = HiddenField('_ca', validators=required)
    ea_ = HiddenField('_ea', validators=required)
    ec_ = HiddenField('_ec', validators=required)
    or_ = HiddenField('_or', validators=required)


_styles = ['CONVERGENTE', 'DIVERGENTE', 'ACOMODADOR', 'ASIMILADOR']
style_choices = []
for style in _styles:
    style_choices.append((style_to_int(style), style.capitalize()))


class PlacesForm(FlaskForm):
    sex = SelectField(label='Género', choices=[(0, 'Masculino'), (1, 'Femenino')], coerce=int)
    prom = FloatField(label='Promedio', validators=required)
    style = SelectField(label='Estilo', choices=style_choices, coerce=int)

    def validate_prom(self, field):
        if field.data < 6.0 or field.data > 10.0:
            raise ValidationError('El promedio debe estar entre 6.0 y 10.0')


class GendersForm(PlacesForm):
    place = SelectField(label='Género', choices=[(0, 'Paraíso'), (1, 'Turrialba')], coerce=int)
    sex = None


class StylesForm(PlacesForm):
    place = SelectField(label='Género', choices=[(0, 'Paraíso'), (1, 'Turrialba')], coerce=int)
    style = None


reliability_choices = [
    (2, 'Baja'),
    (3, 'Media'),
    (4, 'Alta'),
    (5, 'Muy alta'),
]


def common_choices_network(end):
    return [
        (0, 'Baj' + end),
        (1, 'Medi' + end),
        (2, 'Alt' + end)
    ]


class NetworkForm(FlaskForm):
    r = SelectField('Confiabilidad', choices=reliability_choices, coerce=int)
    l = IntegerField('Enlaces', validators=required)
    ca = SelectField('Capacidad', choices=common_choices_network('a'), coerce=float)
    co = SelectField('Costo', choices=common_choices_network('o'), coerce=float)

    def validate_l(self, field):
        if field.data < 7 or field.data > 20:
            raise ValidationError('Debe ser un valor entre 7 y 20 (inclusive)')


def choices(vals, labels):
    return list(zip(vals, labels))


class ProfessorForm(FlaskForm):
    a = SelectField('Edad', coerce=int, choices=choices([1, 2, 3], ['30 o menos', 'Entre 31 y 51', 'Más de 55']))
    b = SelectField('Sexo', choices=choices(['M', 'F', 'NA'], ['Masculino', 'Femenino', 'Indefinido']))
    c = SelectField('Evaluación propia', choices=choices(['I', 'B', 'A'], ['Principiante', 'Intermedio', 'Avanzado']))
    d = SelectField('Número de veces enseñando el curso', coerce=int,
                    choices=choices([1, 2, 3], ['Nunca', 'De 1 a 5', 'Más de 5']))
    e = SelectField('Disciplina', choices=choices(['DM', 'ND', 'O'], ['Desicion-making', 'Network Design', 'Other']))
    f = SelectField('Habilidad usando computadoras', choices=choices(['L', 'M', 'H'], ['Baja', 'Media', 'Alta']))
    g = SelectField('Experiencia con tecnologías web',
                    choices=choices(['N', 'S', 'O'], ['Nunca', 'Algunas veces', 'Con frequencia']))
    h = SelectField('Experiencia con sitios web',
                    choices=choices(['N', 'S', 'O'], ['Nunca', 'Algunas veces', 'Con frequencia']))
