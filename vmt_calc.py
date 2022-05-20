

# SEPARATE IMPORTS BY FUNCTIONS
import os
import random
import xlsxwriter
import numpy as np
import pandas as pd

from set_paths import set_paths
from data_gather import data_gather
from tract_distance import tract_distance
from tract_generation import tract_generation

# Set seed for stochastics to maintain repeatability across results
random.seed(26)

source = "Surf"
# Set Directories
[home_dir, data_dir, output_dir] = set_paths(source)

# Set consumption rate
ldv_rate = 0.32 # in kWh/mi
# Set percentage of electric vehicles on the road
ev_pct = 100 # in %

#Uniform Conditions:
EV_chghome = 100 # in %
EV_chgwork = 0 # in %
EV_chgtransit = 0 # in %

# Create file and folder nomenclature based on initial conditions
tran_set = "A" + str(ev_pct)
if EV_chghome > 0:
    tran_set = tran_set + "_H" + str(EV_chghome)
elif EV_chgwork > 0:
    tran_set = tran_set + "_W" + str(EV_chgwork)
else:
    tran_set = tran_set + "_T" + str(EV_chgtransit)
tran_set = tran_set + "_rs26"

# pre-set day-long and year-long hourly lists
hours_day = [elem for elem in range(24)]
hours_year = [elem for elem in range(8808)]
# pre-set indices for vehicle trip and distance arrays
vtrp = [[1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3],
            [3, 0], [3, 1], [3, 2], [3, 3], [4, 0], [4, 1], [4, 2], [4, 3]]
dist_arr = [[0, 0.5], [0.5, 1.49], [1.5, 2.49], [2.5, 3.49], [3.5, 4.49], [4.5, 5.49],
            [5.5, 10.49], [10.5, 15.49], [15.5, 20.49], [20.5, 30.49], [30.5, 80.00]]

# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)
# Generate List of Tracts
tot_tracts = tract_generation(og_load_list, geo_df, tract_by_county_df)

# THIS NEEDS TO BE AN INPUT
tract_range = [4500, np.size(tot_tracts)]
pt_num = "10_L2"


geo_energy = []
geo_h_energy = []
tot_max_daily_energy = 0
no_room_exists = 0
hh_mem_not_int = 0
supplanted_tracts = 0
single_veh_double_rate = 0

geo_distance = []

os.chdir(output_dir)

for g in range(tract_range[0], tract_range[1]):
    # Function for tract distance calculation
    tract_distance = tract_distance(g, tot_tracts, BTS_df, ACS_df)
    geo_distance.append(tract_distance)


    # Function for household distance calculation



        # function for single-day vehicle trip




# BREAkdownnnnn
