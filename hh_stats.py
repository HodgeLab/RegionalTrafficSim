# SEPARATE IMPORTS BY FUNCTIONS
import os
import sys
import random
import xlsxwriter
import numpy as np

source = sys.argv[1]
pt_num = sys.argv[2]
tr1 = int(sys.argv[3])
tr2 = int(sys.argv[4])

from set_paths import set_paths
# Set Directories
[home_dir, data_dir, output_dir] = set_paths(source)

from data_gather import data_gather
from hh_vtrp_set import hh_vtrp_set
from vacancy_check import vacancy_check
from hh_details_set import hh_details_set
from tract_generation import tract_generation

# Set seed for stochastics to maintain repeatability across results
random.seed(26)

# pre-set day-long and year-long hourly lists
hours_day = [elem for elem in range(24)]
hours_year = [elem for elem in range(8808)]

no_room_exists = 0
hh_mem_not_int = 0
supplanted_tracts = 0
single_veh_double_rate = 0
checks = [no_room_exists, hh_mem_not_int, supplanted_tracts, single_veh_double_rate]

# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)
# Generate List of Tracts
tot_tracts = tract_generation(og_load_list, geo_df, tract_by_county_df)
# Set Directory
os.chdir(output_dir)
wb1 = xlsxwriter.Workbook('Tract_Statistics_p' + pt_num + '.xlsx')
w1 = wb1.add_worksheet('Stats')
w1.write(0, 0, 'Tract Names')
w1.write(0, 1, 'Member Averages')
w1.write(0, 2, 'Vehicle Averages')
w1.write(0, 3, 'Average Vehicle Trips')
w1.write(0, 4, 'Household Count')
w1.write(0, 5, 'Avg Room Count')
w1.write(0, 6, 'Total Pop')
for g in range(tr1, tr2):
    tract_mem = []
    tract_veh = []
    tract_vtrp = []
    # Retrieve tract-specific datasets
    BTS_tract_df = BTS_df[BTS_df["geocode"] == tot_tracts[g]]
    ACS_tract_df = ACS_df[ACS_df["tract_id"] == tot_tracts[g]]
    # Pull tract population and household counts
    tot_pop = BTS_tract_df["tot_pop"].values[0]
    hh_cnt = BTS_tract_df["hh_cnt"].values[0]
    hh_room_cnt = ACS_tract_df["est_tot_rooms"].values[0]
    while hh_room_cnt == 0 or hh_cnt == 0:
        [ACS_tract_df, hh_room_cnt, checks, BTS_tract_df, tot_pop,
         hh_cnt] = vacancy_check(ACS_tract_df, ACS_df, BTS_df, checks,
                                 tot_tracts, hh_room_cnt, hh_cnt, g)
    nan_check = np.isnan(np.sum(BTS_tract_df.values[0]))

    for hh in range(hh_cnt):
        [hh_mem_i, av_veh_i, checks] = hh_details_set(ACS_tract_df, BTS_tract_df, checks)
        tract_mem.append(hh_mem_i)
        tract_veh.append(av_veh_i)

        [vtrp_i, dist_arr] = hh_vtrp_set(BTS_tract_df, hh_mem_i, av_veh_i, nan_check)
        tract_vtrp.append(vtrp_i)

    avg_mem = np.average(tract_mem)
    avg_veh = np.average(tract_veh)
    avg_vtrp = np.average(tract_vtrp)

    w1.write(g+1, 0, tot_tracts[g])
    w1.write(g+1, 1, avg_mem)
    w1.write(g+1, 2, avg_veh)
    w1.write(g+1, 3, avg_vtrp)
    w1.write(g+1, 4, hh_cnt)
    w1.write(g+1, 5, hh_room_cnt)
    w1.write(g+1, 6, tot_pop)

    #print("Average household member in tract: ", tot_tracts[g], " is: ", avg_mem)
    #print("Average household vehicle count in tract: ", tot_tracts[g], " is: ", avg_veh)
    #print("")

wb1.close()
