import random
import numpy as np
def hh_details_set(ACS_tract_df, BTS_tract_df, checks):
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
        checks[0] += 1
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
        checks[1] +=1

    return [hh_mem_i, av_veh_i, checks]
