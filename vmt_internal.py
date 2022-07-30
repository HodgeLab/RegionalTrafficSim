# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:17:57 2022

@author: antho
"""

import os
import sys
import random
import xlsxwriter
import numpy as np
import pandas as pd

from set_paths import set_paths
from data_gather import data_gather
from tract_distance import tract_distance
from tract_generation import tract_generation
# COMMON INPUTS
# source = "Surf"
# trat range: np.size(tot_tracts)]
# def vmt_calc(source, pt_num, tr1, tr2):

source = "Surf"
pt_num = "1"
tr1 = 0
tr2 = 1


# Set seed for stochastics to maintain repeatability across results
random.seed(26)
# Set Directories
[home_dir, data_dir, output_dir] = set_paths(source)

# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)
# Generate List of Tracts
#tot_tracts = tract_generation(og_load_list, geo_df, tract_by_county_df)
os.chdir(data_dir)
tr_df = pd.read_excel("Tx_tracts_all.xlsx")
tot_tracts = tr_df["Tx_Tracts_All"].values

short_trips = 0
hh_mem_not_int = 0
supplanted_tracts = 0
single_veh_double_rate = 0
checks = [short_trips, hh_mem_not_int, supplanted_tracts, single_veh_double_rate]
ldc_track = []

geo_distance = []
g_dist_sum = []
geo_trip_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])
geo_dist_by_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])

os.chdir(output_dir)

for g in range(tr1, tr2):
    track_purpose = np.zeros(9)
    # Function for tract distance calculation
    [tot_tract_distance, checks, track_purpose, tract_dist_by_purp, ldc_track] = tract_distance(g, tot_tracts, BTS_df, ACS_df, checks, track_purpose, ldc_track)
    geo_distance.append(tot_tract_distance)
    g_dist_sum.append(sum(tot_tract_distance))
    geo_trip_purp = pd.concat([geo_trip_purp, pd.DataFrame(track_purpose.reshape(1,-1), columns=list(geo_trip_purp))], ignore_index=True)
    geo_dist_by_purp = pd.concat([geo_dist_by_purp, pd.DataFrame(tract_dist_by_purp.reshape(1,-1), columns=list(geo_dist_by_purp))], ignore_index=True)

print("Total Supplanted Tracts: ", checks[2])
print("Total hh with non-integer members: ", checks[1])
print("Long Distance Average: ", np.average(ldc_track))
print("Total Long-Distance Trips: ", checks[0])

"""
ADDRESS THIS WHEN CONSUMPTION IS INTRODUCED (SEPARATE FUNCTION)
"""

# pre-set day-long and year-long hourly lists
# hours_day = [elem for elem in range(24)]
# hours_year = [elem for elem in range(8808)]

# # Set consumption rate
# ldv_rate = 0.32 # in kWh/mi
# # Set percentage of electric vehicles on the road
# ev_pct = 100 # in %

# #Uniform Conditions:
# EV_chghome = 100 # in %
# EV_chgwork = 0 # in %
# EV_chgtransit = 0 # in %

# Create file and folder nomenclature based on initial conditions
# tran_set = "A" + str(ev_pct)
# if EV_chghome > 0:
#     tran_set = tran_set + "_H" + str(EV_chghome)
# elif EV_chgwork > 0:
#     tran_set = tran_set + "_W" + str(EV_chgwork)
# else:
#     tran_set = tran_set + "_T" + str(EV_chgtransit)
# tran_set = tran_set + "_rs26"
