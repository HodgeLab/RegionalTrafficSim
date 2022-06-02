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

geo_distance = []
g_dist_sum = []
geo_trip_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])
geo_dist_by_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])

os.chdir(output_dir)

for g in range(tr1, tr2):
    track_purpose = np.zeros(9)
    # Function for tract distance calculation
    [tot_tract_distance, checks, track_purpose, tract_dist_by_purp] = tract_distance(g, tot_tracts, BTS_df, ACS_df, checks, track_purpose)
    geo_distance.append(tot_tract_distance)
    g_dist_sum.append(sum(tot_tract_distance))
    geo_trip_purp = geo_trip_purp.append(pd.DataFrame(track_purpose.reshape(1,-1), columns=list(geo_trip_purp)), ignore_index=True)
    geo_dist_by_purp = geo_dist_by_purp.append(pd.DataFrame(tract_dist_by_purp.reshape(1,-1), columns=list(geo_dist_by_purp)), ignore_index=True)
wb1 = xlsxwriter.Workbook('Total_Tract_Distances_p' + pt_num + '.xlsx')
w1 = wb1.add_worksheet('Tract VMT')
w1.write(0, 0, 'Tract Names')
w1.write(0, 1, 'Total Distance')
w1.write_column(1, 0, tot_tracts[tr1:tr2])
w1.write_column(1, 1, g_dist_sum)
wb1.close()

hours_year = [elem for elem in range(8808)]
wb2 = xlsxwriter.Workbook('Tract_Hourly_Distances_p' + pt_num + '.xlsx')
wk2 = wb2.add_worksheet('Hourly VMT')
wk2.write(0, 0, 'Hour')
wk2.write_row(0, 1, tot_tracts[tr1:tr2])
wk2.write_column(1, 0, hours_year)
for g in range(tr1, tr2):
    wk2.write_column(1, (g-tr1)+1, geo_distance[g-tr1])
wb2.close()

wb3 = xlsxwriter.Workbook('Purpose_Tracking_p' + pt_num + '.xlsx')
w3 = wb3.add_worksheet('Trip Purpose')
w3n = wb3.add_worksheet('Trip Dist by Purp')
w3.write(0, 0, 'Tract Names')
w3.write(0, 1, 'Home Trips')
w3.write(0, 2, 'Work Trips')
w3.write(0, 3, 'School Trips')
w3.write(0, 4, 'Medical Trips')
w3.write(0, 5, 'Shopping Trips')
w3.write(0, 6, 'Social Trips')
w3.write(0, 7, 'Transport Trips')
w3.write(0, 8, 'Meal Trips')
w3.write(0, 9, 'Other')
w3.write_column(1, 0, tot_tracts[tr1:tr2])
w3.write_column(1, 1, geo_trip_purp.iloc[:,0])
w3.write_column(1, 2, geo_trip_purp.iloc[:,1])
w3.write_column(1, 3, geo_trip_purp.iloc[:,2])
w3.write_column(1, 4, geo_trip_purp.iloc[:,3])
w3.write_column(1, 5, geo_trip_purp.iloc[:,4])
w3.write_column(1, 6, geo_trip_purp.iloc[:,5])
w3.write_column(1, 7, geo_trip_purp.iloc[:,6])
w3.write_column(1, 8, geo_trip_purp.iloc[:,7])
w3.write_column(1, 9, geo_trip_purp.iloc[:,8])
w3n.write(0, 0, 'Tract Names')
w3n.write(0, 1, 'Home Trip Dist')
w3n.write(0, 2, 'Work Trip Dist')
w3n.write(0, 3, 'School Trip Dist')
w3n.write(0, 4, 'Medical Trip Dist')
w3n.write(0, 5, 'Shopping Trip Dist')
w3n.write(0, 6, 'Social Trip Dist')
w3n.write(0, 7, 'Transport Trip Dist')
w3n.write(0, 8, 'Meal Trip Dist')
w3n.write(0, 9, 'Other Trip Dist')
w3n.write_column(1, 0, tot_tracts[tr1:tr2])
w3n.write_column(1, 1, geo_dist_by_purp.iloc[:,0])
w3n.write_column(1, 2, geo_dist_by_purp.iloc[:,1])
w3n.write_column(1, 3, geo_dist_by_purp.iloc[:,2])
w3n.write_column(1, 4, geo_dist_by_purp.iloc[:,3])
w3n.write_column(1, 5, geo_dist_by_purp.iloc[:,4])
w3n.write_column(1, 6, geo_dist_by_purp.iloc[:,5])
w3n.write_column(1, 7, geo_dist_by_purp.iloc[:,6])
w3n.write_column(1, 8, geo_dist_by_purp.iloc[:,7])
w3n.write_column(1, 9, geo_dist_by_purp.iloc[:,8])
wb3.close()

print("Total Supplanted Tracts: ", checks[2])
print("Total hh with non-integer members: ", checks[1])
print("Total hh where room=0 option existed: ", checks[0])

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
