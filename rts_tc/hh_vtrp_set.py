def hh_vtrp_set(BTS_tract_df, hh_mem_i, av_veh_i, nan_check):
    vtrp_i = -1
    # pre-set indices for vehicle trip and distance arrays
    vtrp = [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4],
                [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]
    dist_arr = [[0, 0.5], [0.5, 1.49], [1.5, 2.49], [2.5, 3.49], [3.5, 4.49], [4.5, 5.49],
                [5.5, 10.49], [10.5, 15.49], [15.5, 20.49], [20.5, 30.49], [30.5, 140]]

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
        vtrp[4].append(BTS_tract_df["vmiles_1mem_4veh"].values[0])
        vtrp[4].append(BTS_tract_df["vtrp_1mem_4veh"].values[0])

        vtrp[5].append(BTS_tract_df["vtrp_2mem_0veh"].values[0])
        vtrp[5].append(BTS_tract_df["vmiles_2mem_0veh"].values[0])
        vtrp[6].append(BTS_tract_df["vtrp_2mem_1veh"].values[0])
        vtrp[6].append(BTS_tract_df["vmiles_2mem_1veh"].values[0])
        vtrp[7].append(BTS_tract_df["vtrp_2mem_2veh"].values[0])
        vtrp[7].append(BTS_tract_df["vmiles_2mem_2veh"].values[0])
        vtrp[8].append(BTS_tract_df["vtrp_2mem_3veh"].values[0])
        vtrp[8].append(BTS_tract_df["vmiles_2mem_3veh"].values[0])
        vtrp[9].append(BTS_tract_df["vtrp_2mem_4veh"].values[0])
        vtrp[9].append(BTS_tract_df["vmiles_2mem_4veh"].values[0])

        vtrp[10].append(BTS_tract_df["vtrp_3mem_0veh"].values[0])
        vtrp[10].append(BTS_tract_df["vmiles_3mem_0veh"].values[0])
        vtrp[11].append(BTS_tract_df["vtrp_3mem_1veh"].values[0])
        vtrp[11].append(BTS_tract_df["vmiles_3mem_1veh"].values[0])
        vtrp[12].append(BTS_tract_df["vtrp_3mem_2veh"].values[0])
        vtrp[12].append(BTS_tract_df["vmiles_3mem_2veh"].values[0])
        vtrp[13].append(BTS_tract_df["vtrp_3mem_3veh"].values[0])
        vtrp[13].append(BTS_tract_df["vmiles_3mem_3veh"].values[0])
        vtrp[14].append(BTS_tract_df["vtrp_3mem_4veh"].values[0])
        vtrp[14].append(BTS_tract_df["vmiles_3mem_4veh"].values[0])

        vtrp[15].append(BTS_tract_df["vtrp_4mem_0veh"].values[0])
        vtrp[15].append(BTS_tract_df["vmiles_4mem_0veh"].values[0])
        vtrp[16].append(BTS_tract_df["vtrp_4mem_1veh"].values[0])
        vtrp[16].append(BTS_tract_df["vmiles_4mem_1veh"].values[0])
        vtrp[17].append(BTS_tract_df["vtrp_4mem_2veh"].values[0])
        vtrp[17].append(BTS_tract_df["vmiles_4mem_2veh"].values[0])
        vtrp[18].append(BTS_tract_df["vtrp_4mem_3veh"].values[0])
        vtrp[18].append(BTS_tract_df["vmiles_4mem_3veh"].values[0])
        vtrp[19].append(BTS_tract_df["vtrp_4mem_4veh"].values[0])
        vtrp[19].append(BTS_tract_df["vmiles_4mem_4veh"].values[0])
    else:
        # AVERAGE ACROSS ALL TX TRACTS:
        vtrp[0].append(0.95) #1m 0v
        vtrp[0].append(2)
        vtrp[1].append(3.83) #1m 1v
        vtrp[1].append(25)
        vtrp[2].append(5.66) #1m 2v
        vtrp[2].append(55)
        vtrp[3].append(5.27) #1m 3v
        vtrp[3].append(42)
        vtrp[4].append(4.97) #1m 4v
        vtrp[4].append(44)

        vtrp[5].append(1.4) #2m 0v
        vtrp[5].append(15)
        vtrp[6].append(4.3) #2m 1v
        vtrp[6].append(38)
        vtrp[7].append(6.15) #2m 2v
        vtrp[7].append(68)
        vtrp[8].append(5.75) #2m 3v
        vtrp[8].append(55)
        vtrp[9].append(5.45) #2m 4v
        vtrp[9].append(45)

        vtrp[10].append(2.07) #3m 0v
        vtrp[10].append(29)
        vtrp[11].append(4.94) #3m 1v
        vtrp[11].append(52)
        vtrp[12].append(6.77) #3m 2v
        vtrp[12].append(82)
        vtrp[13].append(6.38) #3m 3v
        vtrp[13].append(69)
        vtrp[14].append(6.08) #3m 4v
        vtrp[14].append(50)

        vtrp[15].append(2.32) #4m 0v
        vtrp[15].append(32)
        vtrp[16].append(5.19) #4m 1v
        vtrp[16].append(54)
        vtrp[17].append(7.02) #4m 2v
        vtrp[17].append(85)
        vtrp[18].append(6.62) #4m 3v
        vtrp[18].append(72)
        vtrp[19].append(6.32) #4m 4v
        vtrp[19].append(52)

    # Select Estimated Average Vehicle Trips and Mileage from BTS Lookup Table
    for x in range(len(vtrp)):
        if vtrp[x][0] == hh_mem_i and vtrp[x][1] == av_veh_i:
            vtrp_i = vtrp[x][2]
            #hh_vtm_i = vtrp[x][3]
            break
    if vtrp_i == -1:
        print("WE GOT A DIVERGENT, CALL IN THE YA EXPERTS")
        # no reason to track it... this will throw an error

    return [vtrp_i, dist_arr]
