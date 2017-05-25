from .exporters import Exporter

from ..util import nothing, frange


class StudentManager(Exporter):
    id = 'classic_styles'
    table = 'estilos_recinto'
    attrs = ['_ca', '_ec', '_ea', '_or']
    attrs_scope = [len(list(range(6, 37)))] * 4
    classes = ['CONVERGENTE', 'DIVERGENTE', 'ACOMODADOR', 'ASIMILADOR']
    class_column = ['style', ]


class PlaceClassificationManager(Exporter):
    id = 'places'
    table = 'estilos_sexo'
    attrs = ['sex', 'prom', 'style']
    attrs_scope = [2, len(list(frange(6, 10, 0.01))), 4]
    classes = ['Paraiso', 'Turrialba']
    class_column = ['place', ]


class SexClassificationManager(Exporter):
    id = 'genders'
    table = 'estilos_sexo'
    attrs = ['place', 'prom', 'style']
    attrs_scope = [2, len(list(frange(6, 10, 0.01))), 4]
    classes = ['M', 'F']
    class_column = ['sex', ]


class StyleManager(Exporter):
    id = 'styles'
    table = 'estilos_sexo'
    attrs = ['place', 'prom', 'sex']
    attrs_scope = [2, len(list(frange(6, 10, 0.01))), 2]
    classes = ['CONVERGENTE', 'DIVERGENTE', 'ACOMODADOR', 'ASIMILADOR']
    class_column = ['style', ]


class ProfessorManager(Exporter):
    id = 'professors'
    table = 'profesores'
    attrs = [chr(x) for x in range(97, 97 + 8)]
    attrs_scope = [3] * 8
    classes = ['Beginner', 'Intermediate', 'Advanced']
    class_column = ['class']


class NetworkManager(Exporter):
    id = 'networks'
    table = 'redes'
    attrs = ['r', 'l', 'ca', 'co']
    attrs_scope = [4, 14, 3, 3]
    classes = ['A', 'B']
    class_column = ['class']


class CarStolenManager(Exporter):
    id = 'cars'
    table = 'car_stolen'
    attrs = ['color', 'type', 'origin']
    attrs_scope = [2, 2, 2, ]
    classes = ['Yes', 'No']
    class_column = ['stolen']
