import os
import sys
import random
import xlsxwriter
import numpy as np
#import pandas as pd

from set_paths import set_paths
from data_gather import data_gather
from tract_distance import tract_distance
from tract_generation import tract_generation
# COMMON INPUTS
# source = "Surf"
# trat range: np.size(tot_tracts)]
# def vmt_calc(source, pt_num, tr1, tr2):

source = sys.argv[1]
pt_num = sys.argv[2]
tr1 = int(sys.argv[3])
tr2 = int(sys.argv[4])

# Set seed for stochastics to maintain repeatability across results
random.seed(26)
# Set Directories
[home_dir, data_dir, output_dir] = set_paths(source)

# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)
# Generate List of Tracts
tot_tracts = tract_generation(og_load_list, geo_df, tract_by_county_df)

no_room_exists = 0
hh_mem_not_int = 0
supplanted_tracts = 0
single_veh_double_rate = 0
checks = [no_room_exists, hh_mem_not_int, supplanted_tracts, single_veh_double_rate]

# geo_distance = []
g_dist_sum = []

os.chdir(output_dir)

for g in range(tr1, tr2):
    # Function for tract distance calculation
    [tot_tract_distance, checks] = tract_distance(g, tot_tracts, BTS_df, ACS_df, checks)
    # geo_distance.append(tot_tract_distance)
    g_dist_sum.append(sum(tot_tract_distance))
    print("TRACTS COMPLETE: ", g)

wb1 = xlsxwriter.Workbook('Tract_Distances_p' + pt_num + '.xlsx')
w1 = wb1.add_worksheet('Tract VMT')
w1.write(0, 0, 'Tract Names')
w1.write(0, 1, 'Total Distance')
w1.write_column(1, 0, tot_tracts[tr1:tr2])
w1.write_column(1, 1, g_dist_sum)
wb1.close()

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
