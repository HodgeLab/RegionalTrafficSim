# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:10:43 2022

@author: antho


scaling sources:
    https://www2.census.gov/geo/pdfs/reference/ua/2010ua_faqs.pdf
    https://nhts.ornl.gov/assets/DerivedVariables_V1.2.pdf
    https://www.bts.gov/latch-2017-methodology-appendix-d
"""
import os
import xlsxwriter
import numpy as np
import pandas as pd
# Set Directories
source = "Surf"
from set_paths import set_paths
[home_dir, data_dir, output_dir] = set_paths(source)

from data_gather import data_gather
# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)
# Initialize geocode and load lists
geocode = []
dup_list = []
load_list = []
geo_dup_list = []
tot_geo_list = []
# Create list of tracts without duplicates
for i in range(len(og_load_list)):
    loadsplit = og_load_list[i].split('.')
    load_list.append(loadsplit[0])
    geo_load_df = geo_df[geo_df["load_name"] == load_list[i]]
    tract_id = geo_load_df["tract"].values[0]
    tot_geo_list.append(tract_id)
    if tract_id not in geocode:
        geocode.append(tract_id)
    else:
        dup_list.append(load_list[i])
        geo_dup_list.append(tract_id)
# Create a list of all remaining tracts within ERCOT's jurisdiction
ERCOT_tracts = tract_by_county_df["tract_name"]
my_tracts = []
for i in range(len(ERCOT_tracts)):
    tract_id = ERCOT_tracts[i]
    if tract_id not in geocode:
        my_tracts.append(tract_id)
ercotTracts = geocode + my_tracts

hours_year = [elem for elem in range(8808)]

t_df = []
h_df = []
geo_energy = []
geo_t_energy = []
parts = 21

os.chdir(r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database\ABM_Outputs\Ext_Tracts\Full_Texas_TripFixEnergy")
for pt in range(1, parts+1):
    t_df.append(pd.read_excel("Tract_Energies_p" + str(pt) + ".xlsx", 'transit_load_in_kWh'))
    h_df.append(pd.read_excel("Tract_Energies_p" + str(pt) + ".xlsx", 'home_load_in_kWh'))
    t_list = list(t_df[pt-1].columns.values.tolist())
    t_list.remove(t_list[0])

    if pt == 21:
        for i in range(1, 266):
            geo_t_energy.append(t_df[pt-1].iloc[:,i])
            geo_energy.append(h_df[pt-1].iloc[:,i])
    else:
        for i in range(1, 251):
            geo_t_energy.append(t_df[pt-1].iloc[:,i])
            geo_energy.append(h_df[pt-1].iloc[:,i])

wb1 = xlsxwriter.Workbook("ABM_Energy_Output_Transit_v8.xlsx")
wksht = wb1.add_worksheet('load_demand')
wksh2 = wb1.add_worksheet('load_in_kwh')
wksht.write(0,0, 'Hours')
wksht.write_column(1, 0, hours_year)
wksh2.write(0,0, 'Hours')
wksh2.write_column(1, 0, hours_year)

# Splitting loads in similar tracts
for v in range(len(load_list)):
    wksht.write(0, v+1, load_list[v])
    wksh2.write(0, v+1, load_list[v])

    # Retrieve geocode list index to align geo_energy values
    g_in = geocode.index(tot_geo_list[v])
    # How many instances of this geocode exist?
    geo_cnt = tot_geo_list.count(tot_geo_list[v])
    # NEED TO CHANGE TO GEO_ENERGY
    geo_t_energy[g_in] = [elem/geo_cnt for elem in geo_t_energy[g_in]]

# Adding external tracts to closest-distance load buses
for t in range(np.size(geocode), np.size(ercotTracts)):
    current_link_df = links_df[links_df["tract_name"] == ercotTracts[t]]
    load_link = current_link_df["load_name"].values[0]
    current_geo_df = geo_df[geo_df["load_name"] == load_link]
    g_in = current_geo_df.index.values[0]
    for elem in range(len(geo_t_energy[g_in])):
        geo_t_energy[g_in][elem] = geo_t_energy[g_in][elem] + geo_t_energy[t][elem]

# Saving energy values to spreadsheet in both kWh and TAMU ERCOT p.u.
for v in range(len(load_list)):
    g_in = geocode.index(tot_geo_list[v])
    # Capture kWh data after scaling
    wksh2.write_column(1, v+1, geo_t_energy[g_in])

    # Convert to 100MVA base: kWh/100000
    load_energy = [elem/100000 for elem in geo_t_energy[g_in]]
    wksht.write_column(1, v+1, load_energy)
wb1.close()

wb2 = xlsxwriter.Workbook("ABM_Energy_Output_Home_v8.xlsx")
wksht = wb2.add_worksheet('load_demand')
wksh2 = wb2.add_worksheet('load_in_kwh')
wksht.write(0,0, 'Hours')
wksht.write_column(1, 0, hours_year)
wksh2.write(0,0, 'Hours')
wksh2.write_column(1, 0, hours_year)

# Splitting loads in similar tracts
for v in range(len(load_list)):
    wksht.write(0, v+1, load_list[v])
    wksh2.write(0, v+1, load_list[v])

    # Retrieve geocode list index to align geo_energy values
    g_in = geocode.index(tot_geo_list[v])
    # How many instances of this geocode exist?
    geo_cnt = tot_geo_list.count(tot_geo_list[v])
    # NEED TO CHANGE TO GEO_ENERGY
    geo_energy[g_in] = [elem/geo_cnt for elem in geo_energy[g_in]]

# Adding external tracts to closest-distance load buses
for t in range(np.size(geocode), np.size(ercotTracts)):
    current_link_df = links_df[links_df["tract_name"] == ercotTracts[t]]
    load_link = current_link_df["load_name"].values[0]
    current_geo_df = geo_df[geo_df["load_name"] == load_link]
    g_in = current_geo_df.index.values[0]
    for elem in range(len(geo_energy[g_in])):
        geo_energy[g_in][elem] = geo_energy[g_in][elem] + geo_energy[t][elem]

# Saving energy values to spreadsheet in both kWh and TAMU ERCOT p.u.
for v in range(len(load_list)):
    g_in = geocode.index(tot_geo_list[v])
    # Capture kWh data after scaling
    wksh2.write_column(1, v+1, geo_energy[g_in])

    # Convert to 100MVA base: kWh/100000
    load_energy = [elem/100000 for elem in geo_energy[g_in]]
    wksht.write_column(1, v+1, load_energy)
wb2.close()
