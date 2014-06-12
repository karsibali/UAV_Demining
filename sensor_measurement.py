__author__ = 'sarslan'

import numpy as np

def SensorMeasurement( H, objs):
    '''
    %SENSORMEASUREMENT Deteriorate the sensor size and shape
    %   The size and shape of the target is deteriorated to reflect the
    %   randomness in the sensor measurements based on the sensor mode.

    :param H: altitude in meters
    :return : Measured (deteriorated) size and shapes
    '''
    sres = H * 0.0015; # Sensor resolution
    num_objs = objs.shape[0]
    shp_err = np.zeros(num_objs, dtype=int)
    B = np.zeros(num_objs, dtype=int)
    sigma = np.zeros(num_objs, dtype=int)

    shp_err[objs[:,1] >= 8*sres] = 0.4
    shp_err[np.all(np.column_stack((objs[:,1] < 8*sres, objs[:,1] >=5*sres)), axis=1)] = 0.5
    shp_err[np.all(np.column_stack((objs[:,1] < 5*sres, objs[:,1] >=3*sres)), axis=1)] = 0.6
    shp_err[objs[:,1] < 3*sres] = 0.7

    B[objs[:,1] >= 8*sres] = 6
    B[np.all(np.column_stack((objs[:,1] < 8*sres, objs[:,1] >=5*sres)), axis=1)] = 8
    B[np.all(np.column_stack((objs[:,1] < 5*sres, objs[:,1] >=3*sres)), axis=1)] = 10
    B[objs[:,1] < 3*sres] = 12

    sigma[objs[:,1] >= 8*sres] = 6
    sigma[np.all(np.column_stack((objs[:,1] < 8*sres, objs[:,1] >=5*sres)), axis=1)] = 8
    sigma[np.all(np.column_stack((objs[:,1] < 5*sres, objs[:,1] >=3*sres)), axis=1)] = 10
    sigma[objs[:,1] < 3*sres] = 12

    luck_factor = np.random.random()
    measurements = np.zeros((objs.shape[0],2), dtype=int)
    idxs = luck_factor > shp_err
    measurements[idxs, 1] = objs[idxs, 3]
    idxs = np.all(np.column_stack((shp_err - luck_factor > 0.4, shp_err - luck_factor <= 0.6)), axis=1)
    measurements[idxs, 1] = (objs[idxs, 3] + 3) % 5
    idxs = np.all(np.column_stack((shp_err - luck_factor > 0.2, shp_err - luck_factor <= 0.4)), axis=1)
    measurements[idxs, 1] = (objs[idxs, 3] + 2) % 5
    idxs = shp_err - luck_factor <= 0.2
    measurements[idxs, 1] = (objs[idxs, 3] + 1) % 5

    measurements[:, 0] = objs[:, 1] + 0.1 * (B + sigma * np.random.random())

    return measurements