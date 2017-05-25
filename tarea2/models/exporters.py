import sqlite3
import json
from os import path
from os import mkdir

from .. import app


class DatabaseManager:
    conn = None

    @staticmethod
    def open_conn():
        return sqlite3.connect(path.join(app.config['BASEDIR'], 'db.sqlite'))

    @staticmethod
    def select(what_, from_):
        with DatabaseManager.open_conn() as conn:
            c = conn.cursor()
            c.execute('SELECT %s FROM %s;' % (what_, from_,))  # Is that a SQL Injection? lol

            return c.fetchall()

    @staticmethod
    def get_records(cols, table):
        what_ = ', '.join(cols)
        return DatabaseManager.select(what_, table)


class DataFileManager:
    path = path.join(app.config['BASEDIR'], 'data')
    id = ''

    def __init__(self, id):
        self.id = id

    def _full_path(self):
        filename = '{}.json'.format(self.id)
        if not path.exists(self.path):
            mkdir(self.path)
        return path.join(self.path, filename)

    def to_file(self, ds):
        if not self.exists():
            with open(self._full_path(), 'w') as f:
                f.write(json.dumps(ds))

    def from_file(self):
        if self.exists():
            with open(self._full_path(), 'r') as f:
                return json.loads(f.read())
        else:
            raise ValueError(
                'File {} do not exists. You must create the training data set first!'.format(self._full_path()))

    def exists(self):
        return path.isfile(self._full_path())


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
    m = 1
    dataset = {}
    size = 0

    def __init__(self):
        self.file_manager = DataFileManager(self.id)

        if self.file_manager.exists():
            self.import_()
        else:
            self.export()

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
        records = DatabaseManager.get_records(self.attrs + self.class_column, self.table)
        self.size = len(records)
        self.grouped = self.group_by_class(records)
        return self.grouped  # training data grouped by class

    def probability(self, aj=None, class_=None, index=None):
        assert class_
        p = self.dataset
        if aj is not None:
            try:
                p[class_][aj]
            except KeyError:
                assert index is not None
                p[class_][aj] = {'p': 1 / self.attrs_scope[index], 'n_c': 0}
            return (p[class_][aj]['n_c'] + self.m * p[class_][aj]['p']) / (len(self.grouped[class_]) + self.m)

        return len(self.dataset[class_]) / self.size

    def classify(self, vector):
        probabilities = []
        for c in self.classes:
            p = 1
            for i, aj in enumerate(vector):
                p *= self.probability(aj, class_=c, index=i)  # P(aj | c)
            p *= self.probability(class_=c)
            probabilities.append(p)
        argmax = max(probabilities)
        index = probabilities.index(argmax)
        return self.classes[index]

    def train(self, dataset):
        for class_, records in dataset.items():
            self.dataset[class_] = {}
            for row in records:
                for i, column in enumerate(row):
                    if column not in self.dataset[class_]:
                        self.dataset[class_][column] = {}
                        self.dataset[class_][column]['p'] = 1 / self.attrs_scope[i]
                        self.dataset[class_][column]['n_c'] = 0
                    self.dataset[class_][column]['n_c'] += 1

    def export(self):
        assert self.file_manager
        training_data = self.read_grouped_data()
        self.train(training_data)

        self.file_manager.to_file(self.to_json())

    def import_(self):
        assert self.file_manager

        self.from_json(self.file_manager.from_file())

    def to_json(self):
        return {
            'm': self.m,
            'size': self.size,
            'raw_data': self.grouped,
            'dataset': self.dataset
        }

    def from_json(self, dict_):
        self.m = dict_['m']
        self.size = dict_['size']
        self.grouped = dict_['raw_data']
        self.dataset = dict_['dataset']
