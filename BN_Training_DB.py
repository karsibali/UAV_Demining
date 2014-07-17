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
    # The columns are: Type, depth, size, shape, metal content
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
    # Now classify measured sizes
    non_detected_idx = sz_m == 0
    sz_m[non_detected_idx] = -1
    objs[non_detected_idx] = 0  # Mark the objects that cannot be detected as not-mine (0)

    small_idx = np.logical_and(sz_m > 0, sz_m <= 13)
    medium_idx = np.logical_and(sz_m > 13, sz_m <= 24)
    large_idx = np.logical_and(sz_m > 24, sz_m <= 40)
    extralarge_idx = sz_m > 40
    sz_m[small_idx] = 0  # Small
    sz_m[medium_idx] = 1  # Medium
    sz_m[large_idx] = 2  # Large
    sz_m[extralarge_idx] = 3  # Extra-large

    # Convert object features to category indexes
    # We need to do this since the nodes in the BN are all discrete.
    # We need to discretize size and dept variables
    clutter_idx = objs[:, 0] > 2
    mine_idx = objs[:, 0] <= 2
    objs[clutter_idx, 0] = 0  # Mark clutter as not mine
    objs[mine_idx, 0] = 1  # Mark all type of mines as mine
    # Convert depths
    surface_idx = objs[:, 1] == 0
    shallow_idx = np.logical_and(objs[:, 1] > 0, objs[:, 1] <= 12)
    buried_idx = np.logical_and(objs[:, 1] > 12, objs[:, 1] <= 60)
    deep_idx = objs[:, 1] > 60
    objs[surface_idx, 1] = 0  # Surface
    objs[shallow_idx, 1] = 1  # Shallow-buried
    objs[buried_idx, 1] = 2  # Buried
    objs[deep_idx, 1] = 3  # Deep-buried
    # Convert sizes
    small_idx = objs[:, 2] <= 13
    medium_idx = np.logical_and(objs[:, 2] > 13, objs[:, 2] <= 24)
    large_idx = np.logical_and(objs[:, 2] > 24, objs[:, 2] <= 40)
    extralarge_idx = objs[:, 2] > 40
    objs[small_idx, 2] = 0  # Small
    objs[medium_idx, 2] = 1  # Medium
    objs[large_idx, 2] = 2  # Large
    objs[extralarge_idx, 2] = 3  # Extra-large
    # We don't need to convert shapes, since they are already discrete variables
    # We don't need the metal content feature since it is not in BN
    # So, we get rid of metal content feature (last column)
    objs = objs[:, :-1]  # Get rid of the last column

    # Now combine all the feature vectors into one big array.
    # The order of the features must be:
    #   type, depth, size, shape, sensor mode, weather, vegetation, illumination, moisture, shape_m, and size_m
    training_db = np.column_stack((objs, alt_idx, env[:, 5], env[:, 4], env[:, 6], env[:, 0], shp_m, sz_m))

    #sio.savemat('BN_training_db', {'samples': training_db[detected_idx]})
    np.savetxt('BN_training_db.txt', training_db, fmt='%2i', delimiter=' ')
