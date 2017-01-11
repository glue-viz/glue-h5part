import os
from qtpy import QtWidgets, compat
from glue.utils.qt import load_ui
from glue.utils import nonpartial
from glue.config import menubar_plugin

from .io import find_n_steps, read_step_to_data


class H5partWidget(QtWidgets.QWidget):
    """
    The main widget that appears in the toolbar.
    """

    def __init__(self, data_collection=None, parent=None):

        super(H5partWidget, self).__init__(parent=parent)

        self.data_collection = data_collection

        self.ui = load_ui('h5part.ui', self,
                          directory=os.path.dirname(__file__))

        # Set up connections for UI elements
        self.ui.button_load.clicked.connect(nonpartial(self.load_file))
        self.ui.value_step.valueChanged.connect(self.set_step)
        self.ui.value_step.setEnabled(False)
        self.ui.text_step.setText('')

        self.data = None
        self.n_steps = None
        self.filename = None

    def load_file(self):
        """
        Open a dialog to set a filename and open the chosen file.
        """

        filename = compat.getopenfilename(parent=self)[0]

        if filename == "":
            return

        self.filename = filename

        # Find how many steps are in the file
        self.n_steps = find_n_steps(filename)

        # Read the first step and create a data object
        self.data = read_step_to_data(filename, step_id=0)

        # Add the data object to the glue data collection
        self.data_collection.append(self.data)

        # Adjust the slider to accommodate the given number of steps
        self.ui.value_step.setMinimum(0)
        self.ui.value_step.setMaximum(self.n_steps - 1)
        self.ui.value_step.setEnabled(True)

        self.ui.text_step.setText("{0:6d}".format(0))

    def set_step(self, step_id):

        # Read in the specified step to a new data object
        data = read_step_to_data(self.filename, step_id=step_id)

        # Replace the values in the original data object - this ensures that
        # the viewers then update the data. If we removed the old dataset
        # and added the new one to the data collection, the existing viewers
        # would not know to show the new data object.
        self.data.update_values_from_data(data)

        self.ui.text_step.setText("{0:6d}".format(step_id))


@menubar_plugin("Load and browse h5part file")
def h5part_plugin(session, data_collection):
    h5part_widget = H5partWidget(data_collection=data_collection)
    toolbar = QtWidgets.QToolBar()
    toolbar.addWidget(h5part_widget)
    session.application.addToolBar(toolbar)
