import os
import h5py
from glue.core import Data
from qtpy import QtWidgets, compat
from glue.utils.qt import load_ui
from glue.utils import nonpartial
from glue.config import menubar_plugin


class H5partWidget(QtWidgets.QWidget):

    def __init__(self, data_collection=None, parent=None):

        super(H5partWidget, self).__init__(parent=parent)

        self.data_collection = data_collection

        self.ui = load_ui('h5part.ui', self,
                          directory=os.path.dirname(__file__))

        self.ui.button_load.clicked.connect(nonpartial(self.load_file))
        self.ui.value_step.valueChanged.connect(self.set_step)
        self.ui.value_step.setEnabled(False)
        self.ui.text_step.setText('')
        self.data = None
        self.n_steps = None
        self.filename = None

    def load_file(self):

        filename = compat.getopenfilename(parent=self)[0]
        self.filename = filename

        print('FILENAME', filename)

        self.n_steps = find_n_steps(filename)

        self.data = read_step_to_data(filename, step_id=0)

        self.data_collection.append(self.data)

        self.ui.value_step.setMinimum(0)
        self.ui.value_step.setMaximum(self.n_steps - 1)
        self.ui.value_step.setEnabled(True)

        self.ui.text_step.setText("{0:6d}".format(0))

    def set_step(self, step_id):
        self.ui.text_step.setText("{0:6d}".format(step_id))
        data = read_step_to_data(self.filename, step_id=step_id)
        self.data.update_values_from_data(data)


def read_step_to_data(filename, step_id=0):

    f = h5py.File(filename, 'r')

    try:
        group = f['Step#{0}'.format(step_id)]
    except KeyError:
        raise ValueError("Step ID {0} not found in file: {1}".format(step_id, filename))

    data = Data()

    for attribute in group:
        data[attribute] = group[attribute].value

    data.label = os.path.basename(filename.rsplit('.', 1)[0])

    return data


def find_n_steps(filename):

    f = h5py.File(filename, 'r')

    if 'Step#0' not in f:
        raise ValueError("File does not contain Step#n entries")

    # Some groups may not be 'Step' groups so we have to work backwards. The
    # absolute maximum number of steps is the number of groups at the root level.
    n_max = len(f)
    for n_max in range(n_max - 1, -1, -1):
        if 'Step#{0}'.format(n_max) in f:
            return n_max


@menubar_plugin("Load and browse h5part file")
def h5part_plugin(session, data_collection):
    h5part_widget = H5partWidget(data_collection=data_collection)
    toolbar = QtWidgets.QToolBar()
    toolbar.addWidget(h5part_widget)
    session.application.addToolBar(toolbar)
