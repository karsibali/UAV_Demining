__author__ = 'sarslan'
import numpy as np
import scipy.io as sio

import sensor_measurement
import Environment_DB
# from FlightSim import createminefield


def contrast(e):
    env = np.empty(e.shape[0], dtype=int)
    env.fill(-1)
    # If the weather is not clear the contrast is poor
    env[e[:, 5] > 0] = 0
    # If the soil moisture is saturated (>40%) --> poor
    env[e[:, 0] == 2] = 0
    # moisture    vegetation  weather    illumination
    env[e[np.all(np.column_stack((e[:, 0] == 0, e[:, 4] == 0, e[:, 5] == 0)), axis=1)]] = 3
    env[e[np.all(np.column_stack((e[:, 0] == 0, e[:, 4] == 1, e[:, 5] == 0, e[:, 6] == 0)), axis=1)]] = 2
    env[e[np.all(np.column_stack((e[:, 0] == 0, e[:, 4] == 1, e[:, 5] == 0, e[:, 6] == 1)), axis=1)]] = 2
    env[e[np.all(np.column_stack((e[:, 0] == 0, e[:, 4] == 1, e[:, 5] == 0, e[:, 6] == 2)), axis=1)]] = 3
    env[e[np.all(np.column_stack((e[:, 0] == 0, e[:, 4] == 2, e[:, 5] == 0, e[:, 6] == 0)), axis=1)]] = 2
    env[e[np.all(np.column_stack((e[:, 0] == 0, e[:, 4] == 2, e[:, 5] == 0, e[:, 6] == 1)), axis=1)]] = 2
    env[e[np.all(np.column_stack((e[:, 0] == 0, e[:, 4] == 2, e[:, 5] == 0, e[:, 6] == 2)), axis=1)]] = 3
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 0, e[:, 5] == 0, e[:, 6] == 0)), axis=1)]] = 2
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 0, e[:, 5] == 0, e[:, 6] == 1)), axis=1)]] = 3
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 0, e[:, 5] == 0, e[:, 6] == 2)), axis=1)]] = 3
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 1, e[:, 5] == 0, e[:, 6] == 0)), axis=1)]] = 1
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 1, e[:, 5] == 0, e[:, 6] == 1)), axis=1)]] = 1
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 1, e[:, 5] == 0, e[:, 6] == 2)), axis=1)]] = 3
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 2, e[:, 5] == 0, e[:, 6] == 0)), axis=1)]] = 1
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 2, e[:, 5] == 0, e[:, 6] == 1)), axis=1)]] = 1
    env[e[np.all(np.column_stack((e[:, 0] == 1, e[:, 4] == 2, e[:, 5] == 0, e[:, 6] == 2)), axis=1)]] = 1

    return env


if __name__ == '__main__':
    # Load the mine database into a matrix
    # The columns are: Type, size, depth, shape, metal content
    mine_db = np.loadtxt('mine_database.txt', dtype=int, delimiter=' ')

    num_cases = 16000

    # 1. Create samples from mine database
    # 10000 samples from mines and 6000 samples from clutter
    mines = np.random.randint(0, 5000, size=10000)
    clutter = np.random.randint(5000, 8000, size=6000)
    objs = np.concatenate((mines, clutter))
    np.random.shuffle(objs)
    objs = mine_db[objs]

    # 2. Randomly assign environment variables to the samples
    env = Environment_DB.environment(num_cases)

    # 3. Create contrast information for each environment sample
    cont = contrast(env)

    # 4. Create altitudes for each sample. Randomly select from 50 different altitudes
    alts = np.arange(start=500, stop=3000, step=50)
    # Altitude indexes are sensor mode values at the same time.
    alt_idx = np.random.randint(0, alts.size, size=num_cases)
    altitudes = alts[alt_idx]

    # 5. Simulate measurements based on contrast values and altitudes
    sz_m, shp_m = sensor_measurement.sensormeasurement(altitudes, objs, cont)

    # Convert object features to category indexes
    # We need to do this since the nodes in the BN are all discrete.
    # We need to discretize size and dept variables
    objs[objs[:, 0] > 2, 0] = 0  # Mark clutter as not mine
    objs[objs[:, 0] <= 2, 0] = 1  # Mark all type of mines as mine
    # Convert sizes
    objs[objs[:, 1] <= 13, 1] = 0  # Small
    objs[np.logical_and(objs[:, 1] > 13, objs[:, 1] <= 24), 1] = 1  # Medium
    objs[np.logical_and(objs[:, 1] > 24, objs[:, 1] <= 40), 1] = 2  # Large
    objs[objs[:, 1] > 40, 1] = 3  # Extra-large
    # Convert depths
    objs[objs[:, 2] == 0, 2] = 0  # Surface
    objs[np.logical_and(objs[:, 2] > 0, objs[:, 2] <= 12), 2] = 1  # Shallow-burried
    objs[np.logical_and(objs[:, 2] > 12, objs[:, 2] <= 60), 2] = 2  # Burried
    objs[objs[:, 2] > 60, 2] = 0  # Deep-burried
    # We don't need to convert shapes, since they are already discrete variables
    # We don't need the metal content feature since it is not in BN
    # So, we get rid of metal content feature (last column)
    objs = objs[:, :-1]  # Get rid of the last column

    # Now combine all the feature vectors into one big array.
    # The order of the features must be:
    #       type, depth, size, shape, sensor mode, weather, vegetation, illumination, moisture, size_m, and shape_m
    training_db = np.column_stack((objs, alt_idx, env[:, 5], env[:, 4], env[:, 6], env[:, 0], sz_m, shp_m))

    sio.savemat('BN_training_db', {'samples': training_db})

