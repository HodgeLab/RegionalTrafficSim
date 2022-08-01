# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 10:26:23 2022

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
from tract_distance_tc import tract_distance_tc
from tract_generation import tract_generation

source = "Surf" #sys.argv[1]
tr1 = 0 #int(sys.argv[3])
tr2 = 5265 #int(sys.argv[4])

tc_only = True

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

no_room_exists = 0
hh_mem_not_int = 0
supplanted_tracts = 0
single_veh_double_rate = 0
checks = [no_room_exists, hh_mem_not_int, supplanted_tracts, single_veh_double_rate]

geo_distance = []
g_dist_sum = []
geo_trip_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])
geo_dist_by_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])

os.chdir(output_dir)
vtrips_by_tract = np.zeros(5265)

for g in range(tr1, tr2):
    # Function for tract distance calculation
    [checks, nan_check, tot_vtrips] = tract_distance_tc(g, tot_tracts, BTS_df, ACS_df, checks)
    vtrips_by_tract[g] = tot_vtrips
    
print("Annual Total Trip Count (Millions): ", sum(vtrips_by_tract)*365/1000000)
print("Vacancy total: ", checks[2])
