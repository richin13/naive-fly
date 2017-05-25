import sqlite3

from . import app
from os import path, mkdir
import json
from .util import mean, std_dev, probability, style_to_int, gender, nothing, frange, place


class DatabaseManager:
    conn = None

    def open_conn(self):
        return sqlite3.connect(path.join(app.config['BASEDIR'], 'db.sqlite'))

    def select(self, what_, from_):
        with self.open_conn() as conn:
            c = conn.cursor()
            print('SELECT %s FROM %s' % (what_, from_,))
            c.execute('SELECT %s FROM %s;' % (what_, from_,))  # Is that a SQL Injection? lol

            return c.fetchall()


class DataFileManager:
    path = path.join(app.config['BASEDIR'], 'data')

    def _full_path(self, name):
        filename = '{}.json'.format(name)
        if not path.exists(self.path):
            mkdir(self.path)
        return path.join(self.path, filename)

    def to_file(self, id, ds, grouped_ds, force=True):
        files = ((ds, id), (grouped_ds, '{}_grouped'.format(id)))
        for file in files:
            if force or not self.exists(file[1]):
                with open(self._full_path(file[1]), 'w') as f:
                    f.write(json.dumps(file[0]))

    def from_file(self, id):
        paths = [id, '{}_grouped'.format(id)]
        ds = []
        for p in paths:
            if self.exists(p):
                with open(self._full_path(p), 'r') as f:
                    ds.append(json.loads(f.read()))
            else:
                raise ValueError(
                    'File {} do not exists. You must create the training data set first!'.format(self._full_path(id)))
        return ds

    def exists(self, name):
        return path.isfile(self._full_path(name))


class Exporter:
    id = ''
    table = ''
    attrs = []
    attrs_scope = {}
    attrs_freq = []
    attrs_parser = []
    classes = []
    skip = ()
    grouped = None
    class_index = -1  # to be deprecated
    class_column = []

    def __init__(self):
        self.manager = DatabaseManager()

    def group_by_class(self, dataset):
        grouped = {}

        for r in dataset:
            if r[self.class_index] not in grouped:
                grouped[r[self.class_index]] = []
            if self.class_index < 0:
                grouped[r[self.class_index]].append(r[:self.class_index])
            else:
                grouped[r[self.class_index]].append(
                    tuple(map(lambda x: (e for i, e in enumerate(x) if i != self.class_index), r)))

        return grouped

    def read_grouped_data(self):
        what_ = ', '.join(self.attrs + self.class_column)
        records = self.manager.select(what_, self.table)
        dataset = []
        for row in records:
            new_row = []
            for i, c in enumerate(row):
                new_row.append(self.attrs_parser[i](c))
            dataset.append(tuple(new_row))
        return self.group_by_class(dataset)  # training data grouped by class

    def train(self, grouped_dataset):
        c = {}
        for k, v in grouped_dataset.items():
            c[k] = [(mean(r), std_dev(r)) for r in zip(*v)]

        p = {}

        for k, v in c.items():
            # k is the class
            p[k] = {}

            for i, data_col in enumerate(v):
                # data_col is (mean, std-deviation) for the i-th column
                mean_, std_dev_ = data_col

                # The likelihood table
                likelihood = list(map(
                    lambda x: (x[0], list(map(lambda y: (y, probability(y, mean_, std_dev_)), x[1]))),
                    self.attrs_scope.items()
                ))

                p[k][self.attrs[i]] = {}

                for col in likelihood[i][1]:
                    print(col)
                    p[k][self.attrs[i]][col[0]] = col[1]
        return p

    def classify(self, vector):
        dataset, grouped = self.import_()

        for k, v in grouped.items():
            self.attrs_freq.append(1 / len(v))

        predictions = []
        for i, class_ in enumerate(self.classes):
            probability_ = 1
            for j in range(len(self.attrs)):
                print(class_, self.attrs[j], vector[j])
                probability_ *= dataset[class_][self.attrs[j]][vector[j]]
            print(self.attrs_freq)
            predictions.append(probability_ * self.attrs_freq[i])

        return self.classes[predictions.index(max(predictions))]

    def export(self):
        mgr = DataFileManager()

        training_data = self.read_grouped_data()
        p = self.train(training_data)
        mgr.to_file(self.id, p, training_data)

    def import_(self):
        return DataFileManager().from_file(self.id)


class StudentManager(Exporter):
    id = 'classic_styles'
    table = 'estilos_recinto'
    attrs = ['_ca', '_ec', '_ea', '_or']
    attrs_scope = {
        attrs[0]: list(range(6, 37)),
        attrs[1]: list(range(6, 37)),
        attrs[2]: list(range(6, 37)),
        attrs[3]: list(range(6, 37)),
    }
    attrs_parser = [nothing, nothing, nothing, nothing]
    classes = ['CONVERGENTE', 'DIVERGENTE', 'ACOMODADOR', 'ASIMILADOR']
    class_column = ['style', ]


class PlaceClassificationManager(Exporter):
    id = 'places'
    table = 'estilos_sexo'
    attrs = ['sex', 'prom', 'style']
    attrs_scope = {
        attrs[0]: (0, 1),
        attrs[1]: list(frange(6, 10, 0.01)),
        attrs[2]: (0, 1, 2, 3),
    }
    attrs_parser = [gender, nothing, style_to_int, nothing]
    classes = ['Paraiso', 'Turrialba']
    class_column = ['place', ]


class SexClassificationManager(Exporter):
    id = 'genders'
    table = 'estilos_sexo'
    attrs = ['place', 'prom', 'style']
    attrs_scope = {
        attrs[0]: (0, 1),
        attrs[1]: list(frange(6, 10, 0.01)),
        attrs[2]: (0, 1, 2, 3),
    }
    attrs_parser = [place, nothing, style_to_int, nothing]
    classes = ['M', 'F']
    class_column = ['sex', ]


class Classifier:
    manager = None
    columns = []

    def __init__(self, manager, valid_form):
        self.manager = manager
        self.form = valid_form

    def get_class(self):
        e_vector = []  # The vector to classify
        for col in self.get_columns():
            e_vector.append(str(self.form.data[col]))
        print('Vector to classify is: {}'.format(e_vector))
        return self.manager.classify(e_vector)

    def get_columns(self):
        if len(self.columns) == 0:
            return self.manager.attrs
        return self.columns
