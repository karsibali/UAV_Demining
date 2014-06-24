__author__ = 'sarslan'

import numpy as np


def sensormeasurement(H, objs):
    """
    % SENSORMEASUREMENT Deteriorate the sensor size and shape
    %   The size and shape of the target is deteriorated to reflect the
    %   randomness in the sensor measurements based on the sensor mode.

    :param objs: The objects to be deteriorated
    :param H: altitude in meters
    :return : Measured (deteriorated) size and shapes in the form of a 2D array
              where first column is the size and second column is the shape
    """
    objs = objs[objs[:, 2] <= 12]  # The sensor can detect only shallow burried (depth <= 12cm) objects
    sres = H * 0.0015  # Sensor resolution
    num_objs = objs.shape[0]
    shp_err = np.zeros(num_objs)
    B = np.zeros(num_objs)
    sigma = np.zeros(num_objs)

    shp_err[objs[:, 1] >= 8 * sres] = 0.4
    shp_err[np.all(np.column_stack((8 * sres > objs[:, 1], objs[:, 1] >= 5 * sres)), axis=1)] = 0.5
    shp_err[np.all(np.column_stack((5 * sres > objs[:, 1], objs[:, 1] >= 3 * sres)), axis=1)] = 0.6
    shp_err[objs[:, 1] < 3 * sres] = 0.7

    B[objs[:, 1] >= 8 * sres] = 10
    B[np.all(np.column_stack((8 * sres > objs[:, 1], objs[:, 1] >= 5 * sres)), axis=1)] = 20
    B[np.all(np.column_stack((5 * sres > objs[:, 1], objs[:, 1] >= 3 * sres)), axis=1)] = 30
    B[objs[:, 1] < 3 * sres] = 40

    sigma[objs[:, 1] >= 8 * sres] = 10
    sigma[np.all(np.column_stack((8 * sres > objs[:, 1], objs[:, 1] >= 5 * sres)), axis=1)] = 20
    sigma[np.all(np.column_stack((5 * sres > objs[:, 1], objs[:, 1] >= 3 * sres)), axis=1)] = 30
    sigma[objs[:, 1] < 3 * sres] = 40

    luck_factor = np.random.random(num_objs)
    meas_shape = np.zeros(num_objs, dtype=int)
    diff = shp_err - luck_factor
    idxs = diff < 0
    meas_shape[idxs] = objs[idxs, 3]
    idxs = np.logical_and(0 <= diff, diff <= 0.2)
    meas_shape[idxs] = (objs[idxs, 3] + 1) % 5
    idxs = np.logical_and(0.2 < diff, diff <= 0.4)
    meas_shape[idxs] = (objs[idxs, 3] + 2) % 5
    idxs = np.logical_and(0.4 < diff, diff <= 0.6)
    meas_shape[idxs] = (objs[idxs, 3] + 3) % 5
    idxs = 0.6 < diff
    meas_shape[idxs] = (objs[idxs, 3] + np.random.randint(5)) % 5

    meas_size = objs[:, 1] + 0.1 * (B + sigma * np.random.random())

    return (meas_size, meas_shape)