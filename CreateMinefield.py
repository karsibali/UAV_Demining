__author__ = 'sarslan'

import numpy as np
import scipy.io as sio

mines = np.random.randint(1, 5001, size=10000)
clutter = np.random.randint(5001, 8001, size=6000)
objs = np.concatenate((mines, clutter))

obj_idx = np.arange(160000)
np.random.shuffle(obj_idx)
minefield = np.zeros(160000, dtype=int)
minefield[obj_idx[:objs.size]] = objs
minefield = np.reshape(minefield, [400, 400])

sio.savemat('minefield', {'mineF':minefield})
np.savetxt('minefield.txt', minefield, fmt='%i', delimiter=' ')
