__author__ = 'sarslan'

import numpy as np

## Object Types and number of objects in each type
NUM_OBJS = 8000
FEATURES = 5    # Type, depth, size, shape, metal content,
APM = 0         # Anti-Personnel Mines
APM_num = 1320
ATM = 1         # Anti-Tank Mines
ATM_num = 2456
UXO = 2         # Unexploded Ordnance
UXO_num = 1224
CLUT = 3        # Clutter - mine like objects
CLUT_num = 3000

## Depth categories and number of objects in each category
surface = np.empty(3136, dtype=int)
surface.fill(0)
shallow = np.random.randint(1, 13, size=2981)
buried = np.random.randint(13, 61, size=1083)
deep = np.random.randint(61, 100, size=800)
depths = np.concatenate((surface, shallow, buried, deep))

## Size categories and number of objects in each category
small = np.random.randint(3, 14, size=3102)
medium = np.random.randint(14, 25, size=2510)
large = np.random.randint(25, 41, size=2316)
xlarge = np.random.randint(41, 100, size=72)
sizes = np.concatenate((small, medium, large, xlarge))

## Shape categories and number of objects in each category
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

## Metal content categories and number of objects in each category
no_metal = np.random.randint(0, 4, size=2184)
low_metal = np.random.randint(4, 201, size=4129)
high_metal = np.random.randint(201, 500, size=1687)
metal_content = np.concatenate((no_metal, low_metal, high_metal))

## Create an empty array for objects
## First column is the type of the object.
mines = np.empty([NUM_OBJS, FEATURES], dtype=int)
mines[:APM_num, 0] = APM
mines[APM_num:APM_num + ATM_num, 0] = ATM
mines[APM_num + ATM_num:APM_num + ATM_num + UXO_num, 0] = UXO
mines[-CLUT_num:, 0] = CLUT

## Second column is the depth
## Dept values are assigned to the objects the same way as in sizes.
APM_depth_idxs = np.arange(8000)
np.random.shuffle(APM_depth_idxs[:3136+2981]) # APMs are either surface or shallow.
mines[:APM_num, 1] = depths[APM_depth_idxs[:APM_num]]

ATM_depth_idxs = APM_depth_idxs[APM_num:] # Get the remaining depth indexes
ATM_depth_idxs = ATM_depth_idxs[ATM_depth_idxs >= (3136)] # Find the shallow, burried and deep-burried from remaining
np.random.shuffle(ATM_depth_idxs)
mines[APM_num:APM_num+ATM_num, 1] = depths[ATM_depth_idxs[:ATM_num]]

rem_idxs = APM_depth_idxs[APM_num:]
UXO_depth_idxs = np.concatenate((rem_idxs[rem_idxs<(3136)], ATM_depth_idxs[ATM_num:]))
np.random.shuffle(UXO_depth_idxs)
mines[APM_num+ATM_num:APM_num+ATM_num+UXO_num, 1] = depths[UXO_depth_idxs[:UXO_num]]

mines[-CLUT_num:, 1] = depths[UXO_depth_idxs[UXO_num:]]

## Third column is size
APM_size_idxs = np.arange(NUM_OBJS)
# APMs are either small or medium. Shuffle the small and medium sizes and
# assign these sizes to the APMs.
np.random.shuffle(APM_size_idxs[:3102+2510])
mines[:APM_num, 2] = sizes[APM_size_idxs[:APM_num]]

ATM_size_idxs = APM_size_idxs[APM_num:] # Get the remaining sizes after assigning to APMs
ATM_size_idxs = ATM_size_idxs[ATM_size_idxs >= 3102] # Find the ones that are not small
np.random.shuffle(ATM_size_idxs) #Shuffle the indexes and assign the first ATM_num to the objects
mines[APM_num:APM_num + ATM_num, 2] = sizes[ATM_size_idxs[:ATM_num]]

rem_idxs = APM_size_idxs[APM_num:] # The remaining sizes will be assigned  to the remaining objects (UXO and CLUT)
rem_idxs = np.concatenate((rem_idxs[rem_idxs<3102], ATM_size_idxs[ATM_num:]))
np.random.shuffle(rem_idxs)
mines[APM_num + ATM_num:, 2] = sizes[rem_idxs]

## Fourth column is shape
shape_idxs = np.arange(8000)
np.random.shuffle(shape_idxs[:3676+688+1320]) # APMs are cylinder, box or sphere
mines[:APM_num, 3] = shapes[shape_idxs[:APM_num]]

shape_idxs = shape_idxs[APM_num:]
np.random.shuffle(shape_idxs)

mines[APM_num:, 3] = shapes[shape_idxs]

metal_idxs = np.arange(8000)
np.random.shuffle(metal_idxs)

## Fifth column is metal content.
mines[:, 4] = metal_content[metal_idxs]

np.savetxt('mine_database.txt', mines, fmt='%i', delimiter=' ')
