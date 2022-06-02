import os
import sys
import random
import xlsxwriter
import numpy as np
import pandas as pd

from set_paths import set_paths
from data_gather import data_gather
from tract_generation import tract_generation
# Set seed for stochastics to maintain repeatability across results
random.seed(26)
source = "Surf"#sys.argv[1]
# Set Directories
[home_dir, data_dir, output_dir] = set_paths(source)
# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)
# Generate List of Tracts
tot_tracts = tract_generation(og_load_list, geo_df, tract_by_county_df)

# pre-set year-long hourly lists
hours_year = [elem for elem in range(8808)]
# Set consumption rate
ldv_rate = 0.32 # in kWh/mi
# Set percentage of electric vehicles on the road
ev_pct = 100 # in %

geo_distance = pd.DataFrame()

# Pull VMT Data
os.chdir(output_dir)
part_list = os.listdir("./VMT_Outputs")
os.chdir(output_dir + "/VMT_Outputs")
num_parts = np.size(part_list)
for pt in range(num_parts):
    pt_num = str(pt+1)
    dist_df = pd.read_excel("Tract_Hourly_Distances_p" + pt_num + ".xlsx")
    dist_df = dist_df.loc[:,dist_df.columns!='Hour']
    geo_distance = pd.concat([geo_distance, dist_df], axis=1) #append(dist_df.loc[:,dist_df.columns!='Hour'])

# Convert VMT to Energy Consumption
geo_energy = geo_distance.applymap(lambda x: x*ev_pct/100*ldv_rate)

wb1 = xlsxwriter.Workbook('Tract In-Transit Hourly Energy.xlsx')
w1 = wb1.add_worksheet('Tract Energy')
w1.write(0, 0, 'Tract Names')
w1.write_column(1, 0, tot_tracts)
for g in range(np.size(tot_tracts)):
    w1.write(0, g, tot_tracts[g])
    w1.write_column(1, g, geo_energy.iloc[:,g])
wb1.close()
