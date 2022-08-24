# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:17:57 2022

@author: antho
"""

import os
import random
import xlsxwriter
import numpy as np
import pandas as pd

# Set Directories
source = "Surf"
from set_paths import set_paths
# Set Directories
[home_dir, data_dir, output_dir] = set_paths(source)

from data_gather import data_gather
from tract_distance import tract_distance
from tract_generation import tract_generation

evBool = True
pt_num = "5"
tr1 = 0
tr2 = 2

# Set seed for stochastics to maintain repeatability across results
random.seed(26)

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
tot_vtrips = 0
checks = [short_trips, hh_mem_not_int, supplanted_tracts, single_veh_double_rate, tot_vtrips]

geo_distance = []
g_dist_sum = []
geo_trip_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])
geo_dist_by_purp = pd.DataFrame(columns = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"])
geo_energy = []
geo_h_energy = []

os.chdir(output_dir)

for g in range(tr1, tr2):
    track_purpose = np.zeros(9)
    # Function for tract distance calculation
    [tot_tract_distance, tot_tract_hourly_energy, tot_tract_h_hourly_energy, checks, track_purpose, tract_dist_by_purp] = tract_distance(g, tot_tracts, BTS_df, ACS_df, checks, track_purpose, evBool)  
    geo_distance.append(tot_tract_distance)
    g_dist_sum.append(sum(tot_tract_distance))
    geo_trip_purp = pd.concat([geo_trip_purp, pd.DataFrame(track_purpose.reshape(1,-1), columns=list(geo_trip_purp))], ignore_index=True)
    geo_dist_by_purp = pd.concat([geo_dist_by_purp, pd.DataFrame(tract_dist_by_purp.reshape(1,-1), columns=list(geo_dist_by_purp))], ignore_index=True)
    geo_energy.append(tot_tract_hourly_energy)
    geo_h_energy.append(tot_tract_h_hourly_energy)

os.chdir(output_dir)

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

wb3 = xlsxwriter.Workbook('Purpose_Tracking_p' + pt_num + '_GHTripFix.xlsx')
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

wb4 = xlsxwriter.Workbook('Tract_Energies_p' + pt_num + '.xlsx')
w4 = wb4.add_worksheet('transit_load_in_kWh')
w4n = wb4.add_worksheet('home_load_in_kWh')
w4.write(0, 0, 'Hours')
w4.write_column(1, 0, hours_year)
w4n.write(0, 0, 'Hours')
w4n.write_column(1, 0, hours_year)
for g in range(tr1, tr2):
    w4.write(0, g-(tr1-1), tot_tracts[g])
    w4.write_column(1,  g-(tr1-1), geo_energy[g-tr1])
    w4n.write(0, g-(tr1-1), tot_tracts[g])
    w4n.write_column(1, g-(tr1-1), geo_h_energy[g-tr1])
wb4.close()

print("Total Supplanted Tracts: ", checks[2])
print("Total hh with non-integer members: ", checks[1])
print("Annual Total Trip Count (Millions): ", checks[4])
print("Single Vehicles that got double charge rates: ", single_veh_double_rate)

"""
ADDRESS THIS WHEN CONSUMPTION IS INTRODUCED (SEPARATE FUNCTION)
"""
