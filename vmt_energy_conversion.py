import os
import random
import xlsxwriter
import numpy as np
import pandas as pd

# Set Directories
source = "Surf"
from set_paths import set_paths
[home_dir, data_dir, output_dir] = set_paths(source)

from data_gather import data_gather
from tract_generation import tract_generation
# Set seed for stochastics to maintain repeatability across results
random.seed(26)

# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)
# Generate List of Tracts
ercotTracts = tract_generation(og_load_list, geo_df, tract_by_county_df)

# pre-set year-long hourly lists
hours_year = [elem for elem in range(8808)]
# Set consumption rate
ldv_rate = 0.32 # in kWh/mi
# Set percentage of electric vehicles on the road
ev_pct = 100 # in %

geo_distance = pd.DataFrame()

# Pull VMT Data
os.chdir(output_dir)
part_list = os.listdir("./Full_Texas_GenHyp1/VMT")
os.chdir(output_dir + "/Full_Texas_GenHyp1/VMT")
num_parts = np.size(part_list)
for pt in range(num_parts):
    pt_num = str(pt+1)
    dist_df = pd.read_excel("Tract_Hourly_Distances_p" + pt_num + ".xlsx")
    dist_df = dist_df.loc[:,dist_df.columns!='Hour']

    for tract in dist_df.columns:
        if tract not in ercotTracts:
            dist_df = dist_df.loc[:, dist_df.columns!=tract]
    geo_distance = pd.concat([geo_distance, dist_df], axis=1) #append(dist_df.loc[:,dist_df.columns!='Hour'])

# Convert VMT to Energy Consumption
geo_energy = geo_distance.applymap(lambda x: x*ev_pct/100*ldv_rate)

wb1 = xlsxwriter.Workbook('Tract In-Transit Hourly Energy.xlsx')
w1 = wb1.add_worksheet('Tract Energy')
w1.write(0, 0, 'Tract Names')
w1.write_column(1, 0, ercotTracts)
for g in range(np.size(ercotTracts)):
    w1.write(0, g, ercotTracts[g])
    w1.write_column(1, g, geo_energy.iloc[:,g])
wb1.close()
