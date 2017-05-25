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
