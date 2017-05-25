from flask import render_template, request, flash

from . import app
from .forms import StylesClassicForm, PlacesForm, GendersForm, StylesForm, ProfessorForm, NetworkForm
from tarea2.models.managers import StudentManager, PlaceClassificationManager, SexClassificationManager, StyleManager, \
    ProfessorManager, NetworkManager
from .models.classifier import Classifier
from .util import gender_full_text

__all__ = [
    'index', 'classic_styles', 'place', 'gender', 'styles', 'professor', 'network'
]


@app.route('/')
def index():
    return render_template('index.html', context={})


@app.route('/styles/classic', methods=('GET', 'POST'))
def classic_styles():
    ctx = {'title': 'Estilos'}
    form = StylesClassicForm()
    ctx['form'] = form
    if request.method == 'POST':
        if form.validate_on_submit():
            classifier = Classifier(StudentManager(), form)
            classifier.columns = ['ca_', 'ec_', 'ea_', 'or_']
            class_ = classifier.get_class()
            print(class_)
            ctx['result'] = 'Su estilo de aprendizaje es {}'.format(class_)
        else:
            flash('Ocurrió un error. Verifique que tiene activado javascript en su navegador e intente de nuevo.',
                  'error')
    return render_template('styles/classic.html', **ctx)


@app.route('/place', methods=('GET', 'POST'))
def place():
    ctx = {'title': 'Recinto de origen'}
    form = PlacesForm()
    ctx['form'] = form
    if request.method == 'POST':
        if form.validate_on_submit():
            classifier = Classifier(PlaceClassificationManager(), form)
            class_ = classifier.get_class()
            ctx['result'] = 'Su recinto de origen es {}'.format(class_)
        else:
            flash('Ocurrió un error. Verifique que los datos e intente de nuevo.', 'error')

    return render_template('place.html', **ctx)


@app.route('/gender', methods=('GET', 'POST'))
def gender():
    ctx = {'title': 'Sexo del estudiante'}
    form = GendersForm()
    ctx['form'] = form
    if request.method == 'POST':
        if form.validate_on_submit():
            classifier = Classifier(SexClassificationManager(), form)
            class_ = classifier.get_class()
            ctx['result'] = 'Su sexo es {}'.format(gender_full_text(class_))
        else:
            flash('Ocurrió un error. Verifique que los datos e intente de nuevo.', 'error')

    return render_template('gender.html', **ctx)


@app.route('/styles/neo', methods=('GET', 'POST'))
def styles():
    ctx = {'title': 'Estilo de aprendizaje (Simplificado)'}
    form = StylesForm()
    ctx['form'] = form
    if request.method == 'POST':
        if form.validate_on_submit():
            classifier = Classifier(StyleManager(), form)
            class_ = classifier.get_class()
            ctx['result'] = 'Su estilo de aprendizaje es {}'.format(class_.capitalize())
        else:
            print('ATENCIÓN', form.errors)
            flash('Ocurrió un error. Verifique que los datos e intente de nuevo.', 'error')

    return render_template('styles/neo.html', **ctx)


@app.route('/professor', methods=('GET', 'POST'))
def professor():
    ctx = {'title': 'Profesores'}
    form = ProfessorForm()
    ctx['form'] = form
    if request.method == 'POST':
        if form.validate_on_submit():
            classifier = Classifier(ProfessorManager(), form)
            class_ = classifier.get_class()
            ctx['result'] = 'El profesor se clasifica como {}'.format(class_.capitalize())
        else:
            print('ATENCIÓN', form.errors)
            flash('Ocurrió un error. Verifique que los datos e intente de nuevo.', 'error')

    return render_template('professor.html', **ctx)


@app.route('/network', methods=('GET', 'POST'))
def network():
    ctx = {'title': 'Redes'}
    form = NetworkForm()
    ctx['form'] = form
    if request.method == 'POST':
        if form.validate_on_submit():
            classifier = Classifier(NetworkManager(), form)
            class_ = classifier.get_class()
            ctx['result'] = 'La red se clasifica como {}'.format(class_.capitalize())
        else:
            print('ATENCIÓN', form.errors)
            flash('Ocurrió un error. Verifique que los datos e intente de nuevo.', 'error')

    return render_template('network.html', **ctx)
