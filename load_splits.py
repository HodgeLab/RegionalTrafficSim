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
col_per = 250

os.chdir(r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database\ABM_Outputs\Ext_Tracts\Full_Texas_TripFixEnergy")
for pt in range(1, parts):
    t_df.append(pd.read_excel("Tract_Energies_p" + str(pt) + ".xlsx", 'transit_load_in_kWh').iloc[:, 1:col_per+1])
#    h_df.append(pd.read_excel("Tract_Energies_p" + str(pt) + ".xlsx", 'home_load_in_kWh'))
    t_list = list(t_df[pt-1].columns.values.tolist())
    t_list.remove(t_list[0])
    
t_df.append(pd.read_excel("Tract_Energies_p" + str(parts) + ".xlsx", 'transit_load_in_kWh').iloc[:, 1:266])
t_df = pd.concat([t_df[i] for i in range(parts)], axis=1)

wkday_rush_transit_energy = np.zeros(4806)
#wkday_rush_home_energy = np.zeros(4806)
evpk_transit_energy = np.zeros(4806)
#evpk_home_energy = np.zeros(4806)

for i in range(0, np.size(ercotTracts)):
    for day in range(0, 366):
        wknd = day/168 % 1
        for x in range(0, 24):
            # MORNING RUSH
            if x == 8 and wknd <= 0.714:
                # Transit Data
                wkday_rush_transit_energy[i] = wkday_rush_transit_energy[i] + t_df.loc[:, ercotTracts[i]][day*24+x]
                # In-Home Data
#                wkday_rush_home_energy[i] = wkday_rush_home_energy[i] + p1h_df[p1_tracts[i]][day*24+x]
#                wkday_rush_home_energy[i+500] = wkday_rush_home_energy[i+500] = p2h_df[p2_tracts[i]][day*24+x]

            # EVENING PEAK
            if x == 18:
                # Transit Data
                evpk_transit_energy[i] = evpk_transit_energy[i] + t_df.loc[:, ercotTracts[i]][day*24+x]
                # In-Home Data
#                evpk_home_energy[i] = evpk_home_energy[i] + p1h_df[p1_tracts[i]][day*24+x]
#                evpk_home_energy[i+500] = evpk_home_energy[i+500] = p2h_df[p2_tracts[i]][day*24+x]

#wkday_rush_transit_energy = wkday_rush_transit_energy[1:4806]
#evpk_transit_energy = evpk_transit_energy[1:4806]
#wkday_rush_home_energy = wkday_rush_home_energy[1:4806]
#evpk_home_energy = evpk_home_energy[1:4806]

wb1 = xlsxwriter.Workbook('Tract_3Dmap_Analyses.xlsx')
w1 = wb1.add_worksheet('Tract VMT')
w1.write(0, 0, 'Tract Names')
w1.write(0, 1, 'Wkday Rush T')
#w1.write(0, 2, 'Wkday Rush H')
w1.write(0, 3, 'EvPk T')
#w1.write(0, 4, 'EvPk H')
w1.write_column(1, 0, ercotTracts)
w1.write_column(1, 1, wkday_rush_transit_energy)
#w1.write_column(1, 2, wkday_rush_home_energy)
w1.write_column(1, 3, evpk_transit_energy)
#w1.write_column(1, 4, evpk_home_energy)
wb1.close()
