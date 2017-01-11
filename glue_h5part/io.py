import os
import h5py
from glue.core import Data


def read_step_to_data(filename, step_id=0):
    """
    Given a filename and a step ID, read in the data into a new Data object.
    """

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
    """
    Given a filename, find how many steps exist in the file.
    """

    f = h5py.File(filename, 'r')

    if 'Step#0' not in f:
        raise ValueError("File does not contain Step#n entries")

    # Some groups may not be 'Step' groups so we have to work backwards. The
    # absolute maximum number of steps is the number of groups at the root level.
    n_max = len(f)
    for n_max in range(n_max - 1, -1, -1):
        if 'Step#{0}'.format(n_max) in f:
            return n_max
