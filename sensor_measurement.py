__author__ = 'sarslan'

import numpy as np


def sensormeasurement(H, objs, cont):
    """
    % SENSORMEASUREMENT Deteriorate the sensor size and shape
    %   The size and shape of the target is deteriorated to reflect the
    %   randomness in the sensor measurements based on the sensor mode.

    :param objects: The objects to be deteriorated
    :param H: altitude in meters
    :return : Measured (deteriorated) size and shapes in the form of a 2D array
              where first column is the size and second column is the shape
    """

    shp_err_tbl = np.array([[0.5, 0.4, 0.2, 0.1],
                            [0.6, 0.5, 0.3, 0.15],
                            [0.7, 0.6, 0.4, 0.25],
                            [0.8, 0.7, 0.45, 0.3]])

    B_tbl = np.array([[20, 10, 5, 1],
                      [30, 20, 10, 5],
                      [40, 30, 20, 10],
                      [50, 40, 30, 15]])

    sigma_tbl = np.array([[20, 10, 5, 1],
                          [30, 20, 10, 5],
                          [40, 30, 20, 10],
                          [50, 40, 30, 15]])

    objects_idx = np.where(objs[:, 1] <= 12)
    non_detectable_idx = np.where(objs[:, 1] > 12)
    objects = objs[objects_idx]  # The sensor can detect only shallow burried (depth <= 12cm) objects
    sres = H[objects_idx] * 0.0015  # Sensor resolution
    num_objs = objects.shape[0]
    shp_err = np.zeros(num_objs)
    B = np.zeros(num_objs)
    sigma = np.zeros(num_objs)
    contrast = cont[objects_idx]

    # Classify objects according to their sizes
    idxs_0 = objects[:, 2] >= 8 * sres
    idxs_1 = np.logical_and(8 * sres > objects[:, 2], objects[:, 2] >= 5 * sres)
    idxs_2 = np.logical_and(5 * sres > objects[:, 2], objects[:, 2] >= 3 * sres)
    idxs_3 = objects[:, 2] < 3 * sres

    # Assign the shape error, Beta and sigma coefficients from the table according to the contras value
    shp_err[idxs_0] = shp_err_tbl[0, contrast[idxs_0]]
    shp_err[idxs_1] = shp_err_tbl[1, contrast[idxs_1]]
    shp_err[idxs_2] = shp_err_tbl[2, contrast[idxs_2]]
    shp_err[idxs_3] = shp_err_tbl[3, contrast[idxs_3]]

    B[idxs_0] = B_tbl[0, contrast[idxs_0]]
    B[idxs_1] = B_tbl[1, contrast[idxs_1]]
    B[idxs_2] = B_tbl[2, contrast[idxs_2]]
    B[idxs_3] = B_tbl[3, contrast[idxs_3]]

    sigma[idxs_0] = sigma_tbl[0, contrast[idxs_0]]
    sigma[idxs_1] = sigma_tbl[1, contrast[idxs_1]]
    sigma[idxs_2] = sigma_tbl[2, contrast[idxs_2]]
    sigma[idxs_3] = sigma_tbl[3, contrast[idxs_3]]

    # Simulated size measurement values
    meas_size = objects[:, 2] + 0.1 * (B + sigma * np.random.random())

    # Simulated shape measurement values
    luck_factor = np.random.random(num_objs)
    meas_shape = np.zeros(num_objs, dtype=int)
    diff = shp_err - luck_factor
    idxs = diff < 0
    meas_shape[idxs] = objects[idxs, 3]
    idxs = np.logical_and(0 <= diff, diff <= 0.2)
    meas_shape[idxs] = (objects[idxs, 3] + 1) % 5
    idxs = np.logical_and(0.2 < diff, diff <= 0.4)
    meas_shape[idxs] = (objects[idxs, 3] + 2) % 5
    idxs = np.logical_and(0.4 < diff, diff <= 0.6)
    meas_shape[idxs] = (objects[idxs, 3] + 3) % 5
    idxs = 0.6 < diff
    meas_shape[idxs] = (objects[idxs, 3] + np.random.randint(5)) % 5

    ret_size = np.zeros(objs.shape[0])
    ret_size[objects_idx] = meas_size
    ret_size[non_detectable_idx] = 0
    ret_shape = np.zeros(objs.shape[0], dtype=int)
    ret_shape[objects_idx] = meas_shape
    ret_shape[non_detectable_idx] = 0
    return ret_size, ret_shape