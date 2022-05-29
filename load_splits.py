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

# Vehicle trip stdv for South Central Division (BTS LATCH2017 Appendix C)
stdv_urb = 0.8
stdv_sub = 0.8
stdv_rur = 0.5

ldv_rate = 0.32 # in kWh/mi
ev_pct = 100 # percentage of electric vehicles on the road

#Uniform Conditions:
EV_chghome = 100 #in %
EV_chgwork = 0 #in %
EV_chgtransit = 0 #in %

# Create file and folder nomenclature based on initial conditions
tran_set = "A" + str(ev_pct)
if EV_chghome > 0:
    tran_set = tran_set + "_H" + str(EV_chghome)
elif EV_chgwork > 0:
    tran_set = tran_set + "_W" + str(EV_chgwork)
else:
    tran_set = tran_set + "_T" + str(EV_chgtransit)

tran_set = tran_set + "_rs26"
hours_year = [elem for elem in range(8808)]


from set_paths import set_paths
from data_gather import data_gather
from tract_generation import tract_generation

source = "Surf"
[home_dir, data_dir, output_dir] = set_paths(source)

# Gather DataFrames and Load List
[og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df] = data_gather(data_dir)

tot_tracts = tract_generation(og_load_list, geo_df, tract_by_county_df)

# Initialize geocode and load lists
geocode = []
dup_list = []
load_list = []
geo_dup_list = []
tot_geo_list = []

os.chdir(r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database\ABM_Outputs\Ext_Tracts")
p1t_df = pd.read_excel("Tract_Energies_P1_L2.xlsx", 'transit_load_in_kWh')
p1h_df = pd.read_excel("Tract_Energies_P1_L2.xlsx", 'home_load_in_kWh')
p2t_df = pd.read_excel("Tract_Energies_P2_L2.xlsx", 'transit_load_in_kWh')
p2h_df = pd.read_excel("Tract_Energies_P2_L2.xlsx", 'home_load_in_kWh')
p3t_df = pd.read_excel("Tract_Energies_P3_L2.xlsx", 'transit_load_in_kWh')
p3h_df = pd.read_excel("Tract_Energies_P3_L2.xlsx", 'home_load_in_kWh')
p4t_df = pd.read_excel("Tract_Energies_P4_L2.xlsx", 'transit_load_in_kWh')
p4h_df = pd.read_excel("Tract_Energies_P4_L2.xlsx", 'home_load_in_kWh')
p5t_df = pd.read_excel("Tract_Energies_P5_L2.xlsx", 'transit_load_in_kWh')
p5h_df = pd.read_excel("Tract_Energies_P5_L2.xlsx", 'home_load_in_kWh')
p6t_df = pd.read_excel("Tract_Energies_P6_L2.xlsx", 'transit_load_in_kWh')
p6h_df = pd.read_excel("Tract_Energies_P6_L2.xlsx", 'home_load_in_kWh')
p7t_df = pd.read_excel("Tract_Energies_P7_L2.xlsx", 'transit_load_in_kWh')
p7h_df = pd.read_excel("Tract_Energies_P7_L2.xlsx", 'home_load_in_kWh')
p8t_df = pd.read_excel("Tract_Energies_P8_L2.xlsx", 'transit_load_in_kWh')
p8h_df = pd.read_excel("Tract_Energies_P8_L2.xlsx", 'home_load_in_kWh')
p9t_df = pd.read_excel("Tract_Energies_P9_L2.xlsx", 'transit_load_in_kWh')
p9h_df = pd.read_excel("Tract_Energies_P9_L2.xlsx", 'home_load_in_kWh')
p10t_df = pd.read_excel("Tract_Energies_P10_L2.xlsx", 'transit_load_in_kWh')
p10h_df = pd.read_excel("Tract_Energies_P10_L2.xlsx", 'home_load_in_kWh')

p1_tracts = list(p1t_df.columns.values.tolist())
p2_tracts = list(p2t_df.columns.values.tolist())
p3_tracts = list(p3t_df.columns.values.tolist())
p4_tracts = list(p4t_df.columns.values.tolist())
p5_tracts = list(p5t_df.columns.values.tolist())
p6_tracts = list(p6t_df.columns.values.tolist())
p7_tracts = list(p7t_df.columns.values.tolist())
p8_tracts = list(p8t_df.columns.values.tolist())
p9_tracts = list(p9t_df.columns.values.tolist())
p10_tracts = list(p10t_df.columns.values.tolist())

wkday_rush_transit_energy = np.zeros(4806)
wkday_rush_home_energy = np.zeros(4806)

evpk_transit_energy = np.zeros(4806)
evpk_home_energy = np.zeros(4806)

tot_tracts2 = (p1_tracts[1:501] + p2_tracts[1:501] + p3_tracts[1:501]
    + p4_tracts[1:501] + p5_tracts[1:501] + p6_tracts[1:501] + p7_tracts[1:501]
    + p8_tracts[1:501] + p9_tracts[1:501] + p10_tracts[1:310])

for i in range(1, 501):
    for day in range(1, 366):
        wknd = day/168 % 1
        for x in range(0, 24):
            # MORNING RUSH
            if x == 8 and wknd <= 0.714:
                # Transit Data
                wkday_rush_transit_energy[i] = wkday_rush_transit_energy[i] + p1t_df[p1_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+500] = wkday_rush_transit_energy[i+500] = p2t_df[p2_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+1000] = wkday_rush_transit_energy[i+1000] = p3t_df[p3_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+1500] = wkday_rush_transit_energy[i+1500] = p4t_df[p4_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+2000] = wkday_rush_transit_energy[i+2000] = p5t_df[p5_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+2500] = wkday_rush_transit_energy[i+2500] = p6t_df[p6_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+3000] = wkday_rush_transit_energy[i+3000] = p7t_df[p7_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+3500] = wkday_rush_transit_energy[i+3500] = p8t_df[p8_tracts[i]][day*24+x]
                wkday_rush_transit_energy[i+4000] = wkday_rush_transit_energy[i+4000] = p9t_df[p9_tracts[i]][day*24+x]
                # In-Home Data
                wkday_rush_home_energy[i] = wkday_rush_home_energy[i] + p1h_df[p1_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+500] = wkday_rush_home_energy[i+500] = p2h_df[p2_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+1000] = wkday_rush_home_energy[i+1000] = p3h_df[p3_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+1500] = wkday_rush_home_energy[i+1500] = p4h_df[p4_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+2000] = wkday_rush_home_energy[i+2000] = p5h_df[p5_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+2500] = wkday_rush_home_energy[i+2500] = p6h_df[p6_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+3000] = wkday_rush_home_energy[i+3000] = p7h_df[p7_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+3500] = wkday_rush_home_energy[i+3500] = p8h_df[p8_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+4000] = wkday_rush_home_energy[i+4000] = p9h_df[p9_tracts[i]][day*24+x]
                        
            # EVENING PEAK
            if x == 18:
                # Transit Data
                evpk_transit_energy[i] = evpk_transit_energy[i] + p1t_df[p1_tracts[i]][day*24+x]
                evpk_transit_energy[i+500] = evpk_transit_energy[i+500] = p2t_df[p2_tracts[i]][day*24+x]
                evpk_transit_energy[i+1000] = evpk_transit_energy[i+1000] = p3t_df[p3_tracts[i]][day*24+x]
                evpk_transit_energy[i+1500] = evpk_transit_energy[i+1500] = p4t_df[p4_tracts[i]][day*24+x]
                evpk_transit_energy[i+2000] = evpk_transit_energy[i+2000] = p5t_df[p5_tracts[i]][day*24+x]
                evpk_transit_energy[i+2500] = evpk_transit_energy[i+2500] = p6t_df[p6_tracts[i]][day*24+x]
                evpk_transit_energy[i+3000] = evpk_transit_energy[i+3000] = p7t_df[p7_tracts[i]][day*24+x]
                evpk_transit_energy[i+3500] = evpk_transit_energy[i+3500] = p8t_df[p8_tracts[i]][day*24+x]
                evpk_transit_energy[i+4000] = evpk_transit_energy[i+4000] = p9t_df[p9_tracts[i]][day*24+x]
                # In-Home Data
                evpk_home_energy[i] = evpk_home_energy[i] + p1h_df[p1_tracts[i]][day*24+x]
                evpk_home_energy[i+500] = evpk_home_energy[i+500] = p2h_df[p2_tracts[i]][day*24+x]
                evpk_home_energy[i+1000] = evpk_home_energy[i+1000] = p3h_df[p3_tracts[i]][day*24+x]
                evpk_home_energy[i+1500] = evpk_home_energy[i+1500] = p4h_df[p4_tracts[i]][day*24+x]
                evpk_home_energy[i+2000] = evpk_home_energy[i+2000] = p5h_df[p5_tracts[i]][day*24+x]
                evpk_home_energy[i+2500] = evpk_home_energy[i+2500] = p6h_df[p6_tracts[i]][day*24+x]
                evpk_home_energy[i+3000] = evpk_home_energy[i+3000] = p7h_df[p7_tracts[i]][day*24+x]
                evpk_home_energy[i+3500] = evpk_home_energy[i+3500] = p8h_df[p8_tracts[i]][day*24+x]
                evpk_home_energy[i+4000] = evpk_home_energy[i+4000] = p9h_df[p9_tracts[i]][day*24+x]
    
for i in range(1, 306):
    for day in range(1, 366):
        wknd = day/168 % 1
        for x in range(0, 24):
            # MORNING RUSH
            if x == 8 and wknd <= 0.714:    
                wkday_rush_transit_energy[i+4500] = wkday_rush_transit_energy[i+4500] = p10t_df[p10_tracts[i]][day*24+x]
                wkday_rush_home_energy[i+4500] = wkday_rush_home_energy[i+4500] = p10h_df[p10_tracts[i]][day*24+x]                
            if x == 18:               
                evpk_transit_energy[i+4500] = evpk_transit_energy[i+4500] = p10t_df[p10_tracts[i]][day*24+x]      
                evpk_home_energy[i+4500] = evpk_home_energy[i+4500] = p10h_df[p10_tracts[i]][day*24+x]    
                
wkday_rush_transit_energy = wkday_rush_transit_energy[1:4806]
evpk_transit_energy = evpk_transit_energy[1:4806]
wkday_rush_home_energy = wkday_rush_home_energy[1:4806]
evpk_home_energy = evpk_home_energy[1:4806]

wb1 = xlsxwriter.Workbook('Tract_3Dmap_Analyses.xlsx')
w1 = wb1.add_worksheet('Tract VMT')
w1.write(0, 0, 'Tract Names')
w1.write(0, 1, 'Wkday Rush T')
w1.write(0, 2, 'Wkday Rush H')
w1.write(0, 3, 'EvPk T')
w1.write(0, 4, 'EvPk H')
w1.write_column(1, 0, tot_tracts2)
w1.write_column(1, 1, wkday_rush_transit_energy)
w1.write_column(1, 2, wkday_rush_home_energy)
w1.write_column(1, 3, evpk_transit_energy)
w1.write_column(1, 4, evpk_home_energy)
wb1.close()