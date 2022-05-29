import os
import sys
import random
import xlsxwriter
import numpy as np
import pandas as pd

from set_paths import set_paths
from tract_generation import tract_generation
# Set seed for stochastics to maintain repeatability across results
random.seed(26)
source = sys.argv[1]
# Set Directories
[home_dir, data_dir, output_dir] = set_paths(source)
# Generate List of Tracts
tot_tracts = tract_generation(og_load_list, geo_df, tract_by_county_df)

# pre-set year-long hourly lists
hours_year = [elem for elem in range(8808)]
# Set consumption rate
ldv_rate = 0.32 # in kWh/mi
# Set percentage of electric vehicles on the road
ev_pct = 100 # in %

# Pull VMT Data
os.chdir(output_dir)
part_list = os.listdir("./VMT_Outputs")
num_parts = np.size(part_list)
for pt in range(num_parts):
    pt_num = str(pt)
    geo_distance.append(pd.read_excel('Tract_Hourly_Distances_p' + pt_num + '.xlsx'))

# Convert VMT to Energy Consumption
geo_energy = [ev_pct/100*ldv_rate*elem for elem in geo_distance]
