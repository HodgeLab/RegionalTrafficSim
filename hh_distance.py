
def hh_distance(hh, BTS_tract_df, ACS_tract_df):
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
