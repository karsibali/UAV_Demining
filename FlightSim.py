__author__ = 'sarslan'

import numpy as np
import scipy.io as sio

from sensor_measurement import *

def createminefield(size):
    """
        Create a simulated square shaped minefield with size
    :param size:
    :return: a minefield
    """
    mines = np.random.randint(1, 5001, size=10000)
    clutter = np.random.randint(5001, 8001, size=6000)
    objs = np.concatenate((mines, clutter))

    obj_idx = np.arange(size**2)
    np.random.shuffle(obj_idx)
    minefield = np.zeros(size**2, dtype=int)
    minefield[obj_idx[:objs.size]] = objs
    minefield = np.reshape(minefield, [size, size])
    return minefield


alts = np.arange(start=500, stop=3000, step=50)
fov = [20, 10]
fld_size = 400
bin_size = 2.5  # size of one bin in meters

mine_field = createminefield(fld_size)

# Load the mine database into a matrix
# The columns are: Type, size, depth, shape, metal content
mine_db = np.loadtxt('mine_database.txt', dtype=int, delimiter=', ')

# % FOV = 20 x 10 deg with 1.5 mrad
# %     = (20 x 0.0175) x (10 x 0.0175) rad
# % FOV_M = FOV x H

FOV = np.zeros([fld_size, fld_size], dtype=int)
measurements = {}
for idx in range(50):
    fov_h = fov[0] * 0.0175 * alts[idx]
    fov_v = fov[1] * 0.0175 * alts[idx]
    bins_x = fov_h / (bin_size * np.sqrt(2))  # number of bins covered diagonally
    bins_x = int(np.ceil(bins_x/2))
    FOV += np.diag(np.diag(mine_field))
    for dx in range(1, bins_x):
        FOV += np.diag(np.diag(mine_field, dx), dx)
        FOV += np.diag(np.diag(mine_field, -dx), -dx)
    R = FOV[FOV != 0]  # Non-empty bins
    objs = mine_db[R,:]
    measurements[idx] = SensorMeasurement(alts[idx], objs)

sio.savemat('measurements', measurements)