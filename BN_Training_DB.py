__author__ = 'sarslan'

import numpy as np

def environment(sze):
    """
        Create a simulated environment to match the simulated minefield.
        The environment data includes:
                sr : soil moisture (%)- dry [0, 10], wet (10, 40], saturated (>40)
                sc : soil composition - very sandy, sandy, high-clay, clay, silt
                su : soil uniformity  - no, yes (uniform)
                sg : magnetic soil    - no, yes (magnetic)
                vg : vegetation       - no-vegetation, sparse, dense
                wt : weather          - clear, overcast, raining
                il : illumination     - low, medium, high
    :param size: One side of the square shaped minefield area
    :return: a 3d array that includes the environment data over minefield
    """
    sr = 0; sc = 1; su = 2; sg = 3; vg = 4; wt = 5; il = 6

    # Moisture (%) categories:
    sr_dry = 0; sr_wet = 1; sr_saturated = 2

    # Compositon categories:
    sc_vs = 0; sc_s = 1; sc_hc = 2; sc_c = 3; sc_s = 4

    # Vegetation categories:
    vg_no = 0; vg_sp = 1; vg_dn = 2

    # Weather categories:
    wt_cl = 0; wt_oc = 1; wt_rn = 2

    # Illumination categories:
    il_lo = 0; il_me = 1; il_hi = 2

    sz = sze ** 2; # Number of cells in a square shaped area

    # moisture_0 = np.zeros(2339, dtype=int)
    # moisture_1 = np.ones(4555, dtype=int)  # dry
    # moisture_2 = np.empty(1606, dytpe=int) # wet
    # moisture_2.fill(sr_saturated)          # saturated
    # moisture = np.concatenate((moisture_0, moisture_1, moisture_2))
    moisture = np.random.randint(3, size=sz)

    # comp_0 = np.zeros(1743, dtype=int) # very sandy
    # comp_1 = np.ones(1724, dtype=int)  # sandy
    # comp_2 = np.emtpy(1688, dtype=int) # high-clay
    # comp_2.fill(sc_hc)
    # comp_3 = np.empty(1647, dtype=int) # clay
    # comp_3.fill(sc_c)
    # comp_4 = np.empty(1698, dtype=int) # silt
    # comp_4 = np.fill(sc_s)
    # composition = np.concatenate((comp_0, comp_1, comp_2, comp_3, comp_4))
    composition = np.random.randint(4, size=sz)

    # mag_0 = np.zeros(6529, dtype=int) # no
    # mag_1 = np.ones(1971, dtype=int)  # yes (magnetic)
    # magnetic = np.concatenate((mag_0, mag_1))
    magnetic = np.random.randint(2, size=sz)

    # veg_0 = np.zeros(2796, dtype=int)  # no vegetation
    # veg_1 = np.ones(2756, dtype=int)   # sparse
    # veg_2 = np.ones(2948, dtype=int)   # dense
    # vegetation = np.concatenate((veg_0, veg_1, veg_2))
    vegetation = np.random.randint(3, size=sz)

    uniformity = np.random.randint(2, size=sz)

    weather = np.random.randint(3, size=sz)

    illumination = np.random.randint(3, size=sz)

    env = np.concatenate((moisture, composition, uniformity, magnetic, vegetation, weather, illumination))
    np.random.shuffle(env)
    return env.reshape((sze, sze, 7))


if __name__ == '__main__':
    