# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 17:24:03 2022
Probabalistic Agent-Based Model Test Script

Calculate daily vehicle miles traveled based on pop. size and demographics
per Census tract (block) for each ERCOT bus load coordinate.

@author: A.J. Sauter
"""
import os
import random
import xlsxwriter
import numpy as np
import pandas as pd

random.seed(26)

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

hours_day = [elem for elem in range(24)]
hours_year = [elem for elem in range(8808)]

vtrp = [[1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3],
            [3, 0], [3, 1], [3, 2], [3, 3], [4, 0], [4, 1], [4, 2], [4, 3]]

dist_arr = [[0, 0.5], [0.5, 1.49], [1.5, 2.49], [2.5, 3.49], [3.5, 4.49], [4.5, 5.49], 
            [5.5, 10.49], [10.5, 15.49], [15.5, 20.49], [20.5, 30.49], [30.5, 80.00]]

# Retrieve load names list
#os.chdir(r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\STAR II Database")
os.chdir(r"/scratch/alpine/ansa1773/STS_Model")
mylist = os.listdir("./Load_Volumes_post")

# Retrieve dataframes from both BTS LATCH and ACS 5-Year Reports
#os.chdir(r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database")
os.chdir(r"/scratch/alpine/ansa1773/STS_Model")
ACS_df = pd.read_excel("ACS_5Y_2016.DP04_Tx_Tracts.xlsx")
BTS_df = pd.read_excel("BTS_LatchB_Pop_NumDailyTrips.xlsx")
links_df = pd.read_excel("Load_Tract_Linkages.xlsx")
tract_by_county_df = pd.read_excel("Tracts_By_County.xlsx")

# Retrieve dataframe for geocodes (tracts for each bus)
geo_df = pd.read_excel("bus_load_blocks.xlsx")

# Initialize geocode and load lists
geocode = []
dup_list = []
load_list = []
geo_dup_list = []
tot_geo_list = []

# Create list of tracts without duplicates
for i in range(len(mylist)):
    loadsplit = mylist[i].split('.')
    load_list.append(loadsplit[0])
    geo_load_df = geo_df[geo_df["load_name"] == load_list[i]]
    tract_id = geo_load_df["tract"].values[0]
    tot_geo_list.append(tract_id)
    if tract_id not in geocode:
        geocode.append(tract_id)
    else:
        dup_list.append(load_list[i])
        geo_dup_list.append(tract_id)

ERCOT_tracts = tract_by_county_df["tract_name"]
my_tracts = []
for i in range(len(ERCOT_tracts)):
    tract_id = ERCOT_tracts[i]
    if tract_id not in geocode:
        my_tracts.append(tract_id)
tot_tracts = geocode + my_tracts
tract_range = [1000, 1500]
pt_num = "3_L2"
geo_energy = []
geo_h_energy = []
tot_max_daily_energy = 0
no_room_exists = 0
hh_mem_not_int = 0
supplanted_tracts = 0
for g in range(tract_range[0], tract_range[1]):
    #os.chdir(r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database\ABM_Outputs")
    os.chdir(r"/scratch/alpine/ansa1773/STS_Model/ABM_Outputs")
    tot_tract_hourly_dist = np.zeros(8808)
    tot_tract_hourly_energy = np.zeros(8808)
    tot_tract_h_hourly_energy = np.zeros(8808)
    tract_home_counts = []    
    BTS_tract_df = BTS_df[BTS_df["geocode"] == tot_tracts[g]] 
    # TO GET SINGLE VALUE OUT: BTS_tract_df["identifier"].values[0]
    ACS_tract_df = ACS_df[ACS_df["tract_id"] == tot_tracts[g]]
    # See BTS note^^
    tot_pop = BTS_tract_df["tot_pop"].values[0]
    hh_cnt = BTS_tract_df["hh_cnt"].values[0]
    hh_room_cnt = ACS_tract_df["est_tot_rooms"].values[0]  

    # Geographical Scaling
    # Incorporate drive-length (energy consumption) scaling by urban/rural area
    urban_group = BTS_df[BTS_df["geocode"] == tot_tracts[g]]["urban_group"].values[0]
    # LATCH REPORT: Urban Groups 1 and 2 are Urban, 3 is Rural
    if urban_group <= 2:
        ug_scale = 0.932 # 6.8% Decrease in Drive Length for Urban Areas
    else:      
        ug_scale = 1.4169 # 41.69% Increase in Drive Length for Rural Areas    

    # In=Home Charging:
    tract_home_counts = list(zip(*tract_home_counts))
    tot_tract_hourly_dist_chg = np.zeros(8808)
    tot_tract_hourly_chg = np.zeros(8808)
    daily_hometrip_pct = np.zeros(24)
    hourly_mi_chg = np.zeros(24)
    dist_per_hour = np.zeros(24)
    
    while hh_room_cnt == 0 or hh_cnt == 0:
        print("Values for: " + str(tot_tracts[g]) + " DO NOT EXIST")
        bad_index = ACS_tract_df.index
        bad_index = bad_index[0]
        good_index = bad_index-1
        ACS_tract_df = ACS_df[good_index:bad_index]
        new_id = ACS_tract_df['tract_id'].values[0]
        new_loc = ACS_tract_df['Geographic Area Name'].values
        hh_room_cnt = ACS_tract_df["est_tot_rooms"].values[0]  
        print("Supplant with: " + str(new_id) + " located in: " + new_loc[0])
        supplanted_tracts +=1
                   
        BTS_tract_df = BTS_df[BTS_df["geocode"] == new_id]
        tot_pop = BTS_tract_df["tot_pop"].values[0]
        hh_cnt = BTS_tract_df["hh_cnt"].values[0]   
        # Iterate by Households (samples) in each tract
        
    nan_check = np.isnan(np.sum(BTS_tract_df.values[0]))
    for i in range(hh_cnt):
        vtrp_i = -1
        surp_energy = 0
        surp_charge = np.zeros(24)
        max_daily_energy = 0
        # CHARGE LEVEL MUST BE RANDOMLY SELECTED, BETWEEN 1 AND 2
        chargeLevel = "L2" 
        # Number of Rooms in Household by weight (ACS 5Yr '16 DP04 Tx Tracts)
        hh_room_pct = [ACS_tract_df["pct_1_rooms"].values[0], ACS_tract_df["pct_2_rooms"].values[0],
                       ACS_tract_df["pct_3_rooms"].values[0], ACS_tract_df["pct_4_rooms"].values[0],
                       ACS_tract_df["pct_5_rooms"].values[0], ACS_tract_df["pct_6_rooms"].values[0],
                       ACS_tract_df["pct_7_rooms"].values[0], ACS_tract_df["pct_8_rooms"].values[0],
                       ACS_tract_df["pct_9p_rooms"].values[0]]
        
        hh_room_ind = [i for i in range(len(hh_room_pct))]
        # Remove instance where no room exists
        if 0 in hh_room_ind:
            hh_room_ind.pop(0)
            hh_room_pct.pop(0)
            # track instances with no room as an option
            no_room_exists += 1          
        hh_room_i = random.choices(hh_room_ind, weights = hh_room_pct, k=1)
        
        # Number of Household Members per Room by weight (ACS 5Yr '16 DP04 Tx Tracts)        
        mem_room_pct = [ACS_tract_df["pct_1_mem"].values[0], ACS_tract_df["pct_1.01-1.5_mem"].values[0], ACS_tract_df["pct_1.51p_mem"].values[0]]
        mem_room_ind = [1, 1.25, 1.5]
        mem_room_i = random.choices(mem_room_ind, weights = mem_room_pct, k=1)
        # Number of Available Household Vehicles by weight (ACS 5Yr '16 DP04 Tx Tracts)
        av_veh_pct = [ACS_tract_df["pct_1_veh"].values[0], ACS_tract_df["pct_2_veh"].values[0], ACS_tract_df["pct_3p_veh"].values[0]]
    
        av_veh_ind = [i for i in range(len(av_veh_pct))]
        av_veh_i = random.choices(av_veh_ind, weights = av_veh_pct, k=1)
        
        #NOTE: meant to be 3+ av vehicles and 9+ hh rooms, we have elected the minimum
        # Calculate Number of Household Members
        hh_mem_i_pre = mem_room_i[0]*hh_room_i[0]
        
        # Cap at 4 household members per BTS LATCH2017 metrics
        if hh_mem_i_pre > 4:
            hh_mem_i = 4
        else:
            hh_mem_i = hh_mem_i_pre
            
        if not isinstance(hh_mem_i, int):
            hh_mem_i = np.round(hh_mem_i)
            # track non-integer hh member instances
            hh_mem_not_int +=1
            
        # Vehicle Trips and Miles Traveled by Household Members and Available Vehicles
        # BTS LATCH 2017 
        # col1: hh_members, col2: av_veh, col3: hh_vtrp, col4: hh_vmt
        # ***WILL BE A CHANGING SET OF VALUES FOR TRIPS AND DISTANCES IN EACH TRACT***

        if nan_check == False:           
            vtrp[0].append(BTS_tract_df["vtrp_1mem_0veh"].values[0])
            vtrp[0].append(BTS_tract_df["vmiles_1mem_0veh"].values[0])
            vtrp[1].append(BTS_tract_df["vtrp_1mem_1veh"].values[0])
            vtrp[1].append(BTS_tract_df["vmiles_1mem_1veh"].values[0])
            vtrp[2].append(BTS_tract_df["vtrp_1mem_2veh"].values[0])
            vtrp[2].append(BTS_tract_df["vmiles_1mem_2veh"].values[0])
            vtrp[3].append(BTS_tract_df["vtrp_1mem_3veh"].values[0]) 
            vtrp[3].append(BTS_tract_df["vmiles_1mem_3veh"].values[0])
            vtrp[4].append(BTS_tract_df["vtrp_2mem_0veh"].values[0]) 
            vtrp[4].append(BTS_tract_df["vmiles_2mem_0veh"].values[0])
            vtrp[5].append(BTS_tract_df["vtrp_2mem_1veh"].values[0]) 
            vtrp[5].append(BTS_tract_df["vmiles_2mem_1veh"].values[0])
            vtrp[6].append(BTS_tract_df["vtrp_2mem_2veh"].values[0]) 
            vtrp[6].append(BTS_tract_df["vmiles_2mem_2veh"].values[0])
            vtrp[7].append(BTS_tract_df["vtrp_2mem_3veh"].values[0])
            vtrp[7].append(BTS_tract_df["vmiles_2mem_3veh"].values[0])
            vtrp[8].append(BTS_tract_df["vtrp_3mem_0veh"].values[0])
            vtrp[8].append(BTS_tract_df["vmiles_3mem_0veh"].values[0])
            vtrp[9].append(BTS_tract_df["vtrp_3mem_1veh"].values[0])
            vtrp[9].append(BTS_tract_df["vmiles_3mem_1veh"].values[0])
            vtrp[10].append(BTS_tract_df["vtrp_3mem_2veh"].values[0])
            vtrp[10].append(BTS_tract_df["vmiles_3mem_2veh"].values[0])
            vtrp[11].append(BTS_tract_df["vtrp_3mem_3veh"].values[0]) 
            vtrp[11].append(BTS_tract_df["vmiles_3mem_3veh"].values[0])
            vtrp[12].append(BTS_tract_df["vtrp_4mem_0veh"].values[0]) 
            vtrp[12].append(BTS_tract_df["vmiles_4mem_0veh"].values[0])
            vtrp[13].append(BTS_tract_df["vtrp_4mem_1veh"].values[0]) 
            vtrp[13].append(BTS_tract_df["vmiles_4mem_1veh"].values[0])
            vtrp[14].append(BTS_tract_df["vtrp_4mem_2veh"].values[0]) 
            vtrp[14].append(BTS_tract_df["vmiles_4mem_2veh"].values[0])
            vtrp[15].append(BTS_tract_df["vtrp_4mem_3veh"].values[0])
            vtrp[15].append(BTS_tract_df["vmiles_4mem_3veh"].values[0])   
        else:
            # AVERAGE ACROSS ALL TX TRACTS: 
            vtrp[0].append(1) #1m 0v
            vtrp[0].append(2)
            vtrp[1].append(4) #1m 1v
            vtrp[1].append(25)
            vtrp[2].append(6) #1m 2v
            vtrp[2].append(55)
            vtrp[3].append(5) #1m 3v
            vtrp[3].append(42)
            vtrp[4].append(4) #2m 0v
            vtrp[4].append(15)
            vtrp[5].append(7) #2m 1v
            vtrp[5].append(38)
            vtrp[6].append(9) #2m 2v
            vtrp[6].append(68)
            vtrp[7].append(8) #2m 3v
            vtrp[7].append(55)
            vtrp[8].append(7) #3m 0v
            vtrp[8].append(29)
            vtrp[9].append(9) #3m 1v
            vtrp[9].append(52)
            vtrp[10].append(12) #3m 2v
            vtrp[10].append(82)
            vtrp[11].append(11) #3m 3v
            vtrp[11].append(69)
            vtrp[12].append(8) #4m 0v 
            vtrp[12].append(32)
            vtrp[13].append(10) #4m 1v
            vtrp[13].append(54)
            vtrp[14].append(13) #4m 2v
            vtrp[14].append(85)
            vtrp[15].append(12) #4m 3v
            vtrp[15].append(72)
     
        # Select Estimated Average Vehicle Trips and Mileage from BTS Lookup Table
        for x in range(len(vtrp)):
            if vtrp[x][0] == hh_mem_i and vtrp[x][1] == av_veh_i[0]:
                vtrp_i = vtrp[x][2]
                hh_vtm_i = vtrp[x][3]
                break
        if vtrp_i == -1:
            print("WE GOT A DIVERGENT, CALL IN THE YA EXPERTS")
            # no reason to track it... this will throw an error
        # Create Vehicle Trip Profiles
        dist_ind = [i for i in range(len(dist_arr))]       
        hh_hourly_dist = np.zeros(24)      
        ann_hourly_dist = np.zeros(8808)
        ann_hourly_energy = np.zeros(8808)
        ann_hourly_home_energy = np.zeros(8808)
        home_hourly_dist = np.zeros(8808) # Track home-trips per hh ONLY
        
        # Iterate for number of days annually    
        for day in range(0, 367): 
            # Temporal Scaling
            # Determine this hour's percentage of one total week
            wknd = day/168 % 1
            # Decide if the hour is on a weekday or a weekend
            if wknd >= 0.714:
                wkday_scale = 1.181 # 18.1% Increase in Drive Length for Weekends
            else:
                wkday_scale = 0.9411 # 5.9% Decrease in Drive Length for Weekdays                   
            # Determine current day of the year 
            day_chk = day/24
            if day_chk <= 31: #January
                month_scale = 0.852
            elif day_chk <= 59: #February
                month_scale = 1.095
            elif day_chk <= 90: #March
                month_scale = 0.945
            elif day_chk <= 120: #April
                month_scale = 1.114
            elif day_chk <= 151: #May
                month_scale = 0.974
            elif day_chk <= 181: #June
                month_scale = 0.995
            elif day_chk <= 212: #July
                month_scale = 1.132
            elif day_chk <= 243: #August
                month_scale = 0.909
            elif day_chk <= 273: #September
                month_scale = 1.062
            elif day_chk <= 304: #October
                month_scale = 0.922
            elif day_chk <= 334: #November
                month_scale = 1.056
            elif day_chk <= 365: #December
                month_scale = 0.962
            else: # January Again (For the Forecast Window)
                month_scale = 0.852                

            start_point = "Home"    
            # Iterate by number of vehicle trips per household        
            for x in range(int(round(vtrp_i))):
                #totvtrips = totvtrips + 1
                wknd_test = day/7 % 1
                if wknd_test >= 0.714:
                    # Weekend Vehicle Trip Purpose by weight (NHTS 2017 Trip Purpose Summary)
                    vtrp_purp_pct = [35.04, 6.83, 5.57, 0.47, 24.98, 11.25, 
                                     5.19, 9.84, 0.83]
                else:
                    # Weekday Vehicle Trip Purpose by weight (NHTS 2017 Trip Purpose Summary)                    
                    vtrp_purp_pct = [34.04, 19.84, 2.7, 1.68, 16.62, 6.28,
                                     10.97, 6.78, 1.09]
                # Vehicle Trip Purpose Index (NHTS 2017 Trip Purpose Summary) 
                vtrp_purp_ind = ["Home","Work", "School", "Med", "Shop", "Social", 
                                 "Transport", "Meals", "Other"]
    
                # To prevent loop trips, remove starting point from weights and outcomes
                start_ind = vtrp_purp_ind.index(start_point)
                vtrp_purp_pct.pop(start_ind)
                vtrp_purp_ind.remove(start_point)
                
                # Select trip purpose
                if x == int(round(vtrp_i))-1:
                    # Last trip must be home each day
                    purp_x = "Home"
                else:
                    purp_x = random.choices(vtrp_purp_ind, weights = vtrp_purp_pct, k=1)
                    purp_x = purp_x[0]                    

                start_point = purp_x
                
                # Determine trip distance and hour based on trip purpose
                if purp_x == "Home":
                    # Vehicle Home-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0.65, 0.45, 0.22, 0.08, 0.12, 0.32, 1.08, 2.96, 2.57,
                                      2.62, 3.85, 4.94, 6.20, 5.28, 6.10, 8.99, 10.95,
                                      12.74, 8.75, 6.97, 5.33, 4.40, 2.71, 1.72]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Home-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [3.3, 14.9, 13.9, 9.9, 8.4, 6.2, 18.1, 9.0, 5.4, 5.6, 5.2]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])
                    
                    # Adjusting to Annual Hour
                    s_t = start_time_x[0]
                    s_h = day*24 + s_t   
                    # Track ONLY home trip distance (for use in home charging scenarios)
                    home_hourly_dist[s_h] = home_hourly_dist[s_h] + vtrp_dist_x
                    
                elif purp_x == "Work":
                    # Vehicle Work-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0.03, 0.00, 0.00, 0.06, 2.32, 6.16, 14.61, 21.76, 
                                      12.74, 6.45, 4.42, 4.13, 6.89, 5.88, 4.16, 3.14, 2.60,
                                      2.03, 0.95, 0.38, 0.38, 0.57, 0.32, 0.06]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Work-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [2.6, 10, 9.3, 7.6, 6.3, 6.0, 19.6, 13.4, 8.2, 9.4, 7.3]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])        
                elif purp_x == "School":
                    # Vehicle School-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0, 0, 0, 0, 0.15, 0.77, 4.78, 13.73, 14.97, 14.66,
                                      10.03, 4.78, 3.55, 3.86, 2.78, 2.01, 5.09, 7.10,
                                      7.72, 2.16, 0.77, 0.46, 0.31, 0.00]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle School-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [3.2, 13, 12, 9.7, 8.8, 6.3, 19.3, 11.7, 4.9, 6.6, 4.4]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])   
                elif purp_x == "Med":
                    # Vehicle Med-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0, 0, 0, 0, 0.38, 0.38, 1.92, 7.31, 11.54, 17.69,
                                      11.15, 6.54, 7.69, 9.62, 8.85, 8.08, 3.85, 1.54, 
                                      1.15, 0.385, 0.77, 0.385, 0, 0]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Med-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [2.9, 9.5, 11.8, 8.2, 8, 7.5, 21.1, 11.3, 7.4, 6.2, 6.2]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])          
                elif purp_x == "Shop":
                    # Vehicle Shop-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0.141, 0, 0, 0, 0.057, 0.311, 1.102, 2.402, 4.747,
                                      7.799, 11.02, 10.455, 9.749, 8.76, 8.223, 8.11, 7.827,
                                      6.782, 5.397, 3.334, 1.978, 1.045, 0.537, 0.198]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Shop-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [8.8, 21.7, 17.7, 11.3, 7.8, 5.7, 13.2, 6.1, 3, 2.4, 2.8]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])               
                elif purp_x == "Social":
                    # Vehicle Social-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0.07, 0.07, 0.07, 0, 0.49, 1.34, 1.9, 3.87, 5.41,
                                      6.04, 6.61, 7.38, 5.62, 6.32, 7.1, 7.1, 8.36, 10.33, 
                                      9.7, 5.55, 3.16, 1.83, 1.12, 0.63]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Social-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [3.4, 12.9, 12.1, 10.3, 8.2, 5.8, 18.6, 8.9, 5.7, 5.4, 8.7]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])  
                elif purp_x == "Transport":
                    # Vehicle Transport-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0.17, 0.17, 0.06, 0, 0.5, 0.94, 4.98, 21.76, 7.03,
                                      3.1, 3.16, 3.27, 3.21, 4.04, 8.53, 11.68, 8.97, 8.19, 
                                      3.77, 2.05, 1.72, 1.61, 0.72, 0.33]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Transport-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [5, 19.5, 15.8, 11.3, 7.6, 6.5, 16.2, 7.5, 4.1, 3.3, 3.1]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])  
                elif purp_x == "Meals":
                    # Vehicle Meals-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0.21, 0.07, 0, 0, 0.35, 0.84, 2.31, 4.20, 4.20,
                                      4.48, 5.46, 12.25, 14.36, 7.42, 5.74, 4.48, 4.9,
                                      7.84, 8.75, 5.81, 3.57, 1.68, 0.84, 0.21]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Meals-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [7.3, 21.4, 17.6, 11.5, 7.9, 6.3, 13.4, 5.6, 3, 3.2, 2.9]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0]) 
                elif purp_x == "Other":
                    # Vehicle Meals-Trip Start Time by weight (NHTS 2017 Trip Start Times)
                    start_time_pct = [0, 0, 0, 0, 0.51, 2.05, 3.59, 7.18, 8.72, 9.74,
                                      8.72, 7.69, 7.69, 7.69, 5.13, 6.67, 5.64, 7.69, 4.62,
                                      2.56, 2.05, 0.51, 0.51, 0.51]
                    start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23]
                    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
                    
                    # Vehicle Other-Trip Distance by weight (NHTS 2017 Trip Distance)
                    vtrp_dist_pct = [4.4, 13, 11.3, 9.9, 6.4, 5.6, 21, 9.9, 5.4, 5.4, 7.7]           
                    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
                    dist_range = dist_range[0]
                    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0]
                                   *random.random()+dist_arr[dist_range][0])

                # Apply Geo and Temp Scaling to Trip Distance
                vtrp_dist_x = vtrp_dist_x*ug_scale*wkday_scale*month_scale
                
                # Add trip distance to total household hourly distance
                hh_hourly_dist[start_time_x[0]] = hh_hourly_dist[start_time_x[0]]+vtrp_dist_x
            
                # Adjusting to Annual Hour
                s_t = start_time_x[0]
                s_h = day*24 + s_t                
                #ann_hourly_dist[s_h] = tract_hourly_dist[s_t]
                ann_hourly_dist[s_h] = ann_hourly_dist[s_h] + vtrp_dist_x
                ann_hourly_energy[s_h] = ann_hourly_energy[s_h] + ev_pct/100*ldv_rate*vtrp_dist_x
            # Find a way to sum up the daily distance values
            
            if EV_chghome > 0:
                hometrip_hour = []
                htrip_energy = []
                hr_full_chg = []
                ext_chg = []
                charge_duration = []
                charge_per_hour = np.zeros(24)
                y = 0
                if chargeLevel == "L1":
                    # Level 1 Charge Rate
                    c_rate = 1.4
                elif chargeLevel == "L2":
                    # Level 2 Charge Rate
                    c_rate = 7.6      
                
                # Include previous day's leftover charging
                if sum(surp_charge) > 0:
                    charge_per_hour = surp_charge
                    surp_charge = np.zeros(24)
                
                # Calculate daily energy per household
                daily_hh_energy = sum(ann_hourly_energy[day*24:(day+1)*24])
                
                for x in range(0, 24):
                    if home_hourly_dist[day*24+x] > 0:
                        hometrip_hour.append(x)
                        htrip_energy.append(sum(ann_hourly_energy[(day*24)+y:(day*24)+(x+1)]) + surp_energy)
                        surp_energy = 0
                        y = x+1
                
                if sum(ann_hourly_energy[day*24+y:(day+1)*24]) > 0:
                    surp_energy = sum(ann_hourly_energy[day*24+y:(day+1)*24]) 
                else:
                    surp_energy = 0            
                # Calc hours of full charge and partial charge
                for n in range(0, np.size(hometrip_hour)):
                    hr_full_chg.append(int(htrip_energy[n]/c_rate))
                    ext_chg.append(htrip_energy[n]/c_rate % 1)
                    # Determine duration of charge 
                    if ext_chg[n] > 0:
                        charge_duration.append(hr_full_chg[n] + 1)
                    else:
                        charge_duration.append(hr_full_chg[n])
                    for x in range(hometrip_hour[n], hometrip_hour[n]+charge_duration[n]):
                        if x < hometrip_hour[n] + hr_full_chg[n]:
                            if x >= 24:
                                j = x - 24
                                surp_charge[j] = surp_charge[j] + c_rate
                            else:
                                charge_per_hour[x] = charge_per_hour[x] + c_rate
                        else:
                            if x >= 24:
                                j = x - 24
                                surp_charge[j] = surp_charge[j] + c_rate*ext_chg[n]
                            else:
                                charge_per_hour[x] = charge_per_hour[x] + c_rate*ext_chg[n]               
                
                if daily_hh_energy > max_daily_energy:
                    max_daily_energy = daily_hh_energy
                    if max_daily_energy > tot_max_daily_energy:
                        tot_max_daily_energy = max_daily_energy
                        tot_charge_per_hour = charge_per_hour
                        tot_surp_energy = surp_energy
                        tot_charge_duration = charge_duration
                        tot_htrip_energy = htrip_energy
                        tot_hometrip_hour = hometrip_hour
                
                ann_hourly_home_energy[day*24:(day+1)*24] = charge_per_hour
                if day == 366:
                    ann_hourly_home_energy[0:24] = ann_hourly_home_energy[0:24] + surp_charge
                    if surp_energy > 0:
                        lst_chg = int(surp_energy/c_rate)
                        lst_ext_chg = surp_energy/c_rate % 1
                        if lst_ext_chg > 0:
                            lst_duration = lst_chg + 1
                            for n in range(lst_duration-1):
                                ann_hourly_home_energy[8807-(lst_duration-n)] = ann_hourly_home_energy[8807-(lst_duration-n)] + c_rate
                            ann_hourly_home_energy[8807] = ann_hourly_home_energy[8807] + lst_ext_chg*c_rate
                        else:
                            lst_duration = lst_chg
                            for n in range(lst_duration-1):
                                ann_hourly_home_energy[8807-(lst_duration-n)] = ann_hourly_home_energy[8807-(lst_duration-n)] + c_rate
            # if abs(sum(ann_hourly_energy) - sum(ann_hourly_home_energy) - surp_energy - sum(surp_charge)) > 5:
            #     breakpoint()
           
        # Sum total annual hourly distance and energy per tract
        tot_tract_hourly_dist = tot_tract_hourly_dist + ann_hourly_dist
        tot_tract_hourly_energy = tot_tract_hourly_energy + ann_hourly_energy
        tot_tract_h_hourly_energy = tot_tract_h_hourly_energy + ann_hourly_home_energy
        if abs(sum(ann_hourly_energy) - sum(ann_hourly_home_energy)) > 1:
            breakpoint()
            print("ann")
        if abs(sum(tot_tract_hourly_energy) - sum(tot_tract_h_hourly_energy)) > 1:
            breakpoint()
            print("tract")

                                          
    geo_energy.append(tot_tract_hourly_energy)   
    geo_h_energy.append(tot_tract_h_hourly_energy)

wb1 = xlsxwriter.Workbook('TEST_Tract_Energies_P' + pt_num + '.xlsx')
w1 = wb1.add_worksheet('transit_load_in_kWh')
w2 = wb1.add_worksheet('home_load_in_kWh')
w1.write(0, 0, 'Hours')
w1.write_column(1, 0, hours_year)
w2.write(0, 0, 'Hours')
w2.write_column(1, 0, hours_year)
for g in range(tract_range[0], tract_range[1]):
    w1.write(0, g-(tract_range[0]-1), tot_tracts[g])
    w1.write_column(1,  g-(tract_range[0]-1), geo_energy[g-tract_range[0]])
    w2.write(0, g-(tract_range[0]-1), tot_tracts[g])
    w2.write_column(1, g-(tract_range[0]-1), geo_h_energy[g-tract_range[0]])
wb1.close()

print("Total Supplanted Tracts: ", supplanted_tracts)
print("Total hh with non-integer members: ", hh_mem_not_int)
print("Total hh where room=0 option existed: ", no_room_exists)

print("Total Max Daily Energy: ", tot_max_daily_energy)
print("Max Day Charge Prof: ", tot_charge_per_hour)
print("Max Day Surp Prof: ", tot_surp_energy)
print("Max Day Charge Durations: ", tot_charge_duration)
print("Max Day Trip Energies: ", tot_htrip_energy)
print("Max Day Hometrip Times: ", tot_hometrip_hour)