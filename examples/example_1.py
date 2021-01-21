#
# This file is part of LS2D.
#
# Copyright (c) 2017-2021 Wageningen University & Research
# Author: Bart van Stratum (WUR)
#
# LS2D is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LS2D is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LS2D.  If not, see <http://www.gnu.org/licenses/>.
#

# Python modules
from datetime import datetime
import subprocess
import shutil
import sys,os

# Third party modules
import matplotlib.pyplot as pl
import numpy as np

pl.close('all'); pl.ion()

# LS2D modules
sys.path.append('/home/bart/meteo/models/LS2D')
import ls2d

settings = {
    'central_lat' : 51.971,
    'central_lon' : 4.927,
    'area_size'   : 1,
    'case_name'   : 'cabauw',
    'era5_path'   : '/home/scratch1/meteo_data/LS2D/',
    'era5_expver' : 1,   # 1=normal ERA5, 5=ERA5 near-realtime
    'start_date'  : datetime(year=2016, month=8, day=15, hour=6),
    'end_date'    : datetime(year=2016, month=8, day=15, hour=18),
    'write_log'   : False,
    'data_source' : 'CDS',
    'ntasks'      : 3
    }

# Download required ERA5 files:
ls2d.download_era5(settings)

# Read ERA5 data, and calculate derived properties (thl, etc.):
era = ls2d.Read_era5(settings)

# Calculate large-scale forcings:
# `n_av` is the number of ERA5 gridpoints (+/-) over which
# the ERA5 variables and forcings are averaged.
era.calculate_forcings(n_av=0, method='2nd')

# Interpolate ERA5 to fixed height grid:
z = np.arange(10, 3000, 20)
les_input = era.interpolate_to_fixed_height(z)

# Plot variables as example:
pl.figure(figsize=(8,8))
sp = 1
for var, data in les_input.items():
    pl.subplot(4,4,sp); sp+=1
    pl.plot(data.T, les_input['z'].T)
    pl.xlabel(var)
    pl.ylabel('z (m)')
pl.tight_layout()
