__author__ = 'sarslan'

import numpy as np

apm_num = 1320
apm = 0
atm_num = 2456
atm = 1
uxo_num = 1224
uxo = 2
clut_num = 3000
clut = 3


surface = np.empty(3136, dtype=int)
surface.fill(0)
shallow = np.random.randint(1, 13, size=2981)
buried = np.random.randint(13, 61, size=1083)
deep = np.random.randint(61, 100, size=800)
depths = np.concatenate((surface, shallow, buried, deep))

small = np.random.randint(3, 14, size=3102)
medium = np.random.randint(14, 25, size=2510)
large = np.random.randint(25, 41, size=2316)
xlarge = np.random.randint(41, 100, size=72)
sizes = np.concatenate((small, medium, large, xlarge))

cylinder = np.empty(3676, dtype=int)
cylinder.fill(0)
box = np.empty(688, dtype=int)
box.fill(1)
sphere = np.empty(1320, dtype=int)
sphere.fill(2)
longslender = np.empty(1224, dtype=int)
longslender.fill(3)
irregular = np.empty(1092, dtype=int)
irregular.fill(4)
shapes = np.concatenate((cylinder, box, sphere, longslender, irregular))

no_metal = np.random.randint(0, 4, size=2184)
low_metal = np.random.randint(4, 201, size=4129)
high_metal = np.random.randint(201, 500, size=1687)
metal_content = np.concatenate((no_metal, low_metal, high_metal))

mines = np.empty([8000, 5], dtype=int)
mines[:apm_num, 0] = apm
mines[apm_num:apm_num + atm_num, 0] = atm
mines[apm_num + atm_num:apm_num + atm_num + uxo_num, 0] = uxo
mines[-clut_num:, 0] = clut

apm_size_idxs = np.arange(8000)
np.random.shuffle(apm_size_idxs[:3102+2510])
mines[:apm_num, 1] = sizes[apm_size_idxs[:apm_num]]

atm_size_idxs = apm_size_idxs[apm_num:]
atm_size_idxs = atm_size_idxs[atm_size_idxs >= 3102]
np.random.shuffle(atm_size_idxs)
mines[apm_num:apm_num + atm_num, 1] = sizes[atm_size_idxs[:atm_num]]

rem_idxs = apm_size_idxs[apm_num:]
rem_idxs = np.concatenate((rem_idxs[rem_idxs<3102], atm_size_idxs[atm_num:]))
np.random.shuffle(rem_idxs)
mines[apm_num + atm_num:, 1] = sizes[rem_idxs]


apm_depth_idxs = np.arange(8000)
np.random.shuffle(apm_depth_idxs[:3136+2981])
mines[:apm_num, 2] = depths[apm_depth_idxs[:apm_num]]

atm_depth_idxs = apm_depth_idxs[apm_num:]
np.random.shuffle(atm_depth_idxs)
mines[apm_num:apm_num+atm_num, 2] = depths[atm_depth_idxs[:atm_num]]

uxo_depth_idxs = atm_depth_idxs[atm_num:]
np.random.shuffle(uxo_depth_idxs)
mines[apm_num+atm_num:apm_num+atm_num+uxo_num, 2] = depths[uxo_depth_idxs[:uxo_num]]

mines[-clut_num:, 2] = depths[uxo_depth_idxs[uxo_num:]]

shape_idxs = np.arange(8000)
np.random.shuffle(shape_idxs[:3676+688+1320])
mines[:apm_num, 3] = shapes[shape_idxs[:apm_num]]

shape_idxs = shape_idxs[apm_num:]
np.random.shuffle(rem_idxs)

mines[apm_num:, 3] = shapes[shape_idxs]

metal_idxs = np.arange(8000)
np.random.shuffle(metal_idxs)

mines[:, 4] = metal_content[metal_idxs]

np.savetxt('mine_database.txt', mines, fmt='%i', delimiter=', ')
