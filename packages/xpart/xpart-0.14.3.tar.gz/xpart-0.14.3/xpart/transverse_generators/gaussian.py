# copyright ############################### #
# This file is part of the Xpart Package.   #
# Copyright (c) CERN, 2021.                 #
# ######################################### #

import numpy as np

def generate_2D_gaussian(num_particles):

    x_norm = np.random.normal(size=num_particles)
    px_norm = np.random.normal(size=num_particles)

    return x_norm, px_norm

