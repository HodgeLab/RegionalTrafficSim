from hh_details_set import hh_details_set
from vtrp_distance import vtrp_distance
from temp_scaling import temp_scaling
from hh_vtrp_set import hh_vtrp_set
import numpy as np
import pandas as pd
def hh_distance(ACS_tract_df, BTS_tract_df, ug_scale, nan_check, checks, track_purpose):
    surp_energy = 0
    surp_charge = np.zeros(24)
    max_daily_energy = 0
    # CHARGE LEVEL MUST BE RANDOMLY SELECTED, EVENTUALLY
    chargeLevel = "L2"
    # Create Vehicle Trip Profiles
    hh_hourly_dist = np.zeros(24)
    ann_hourly_dist = np.zeros(8808)
    # ann_hourly_energy = np.zeros(8808)
    # ann_hourly_home_energy = np.zeros(8808)
    home_hourly_dist = np.zeros(8808) # Track home-trips per hh ONLY

    purp_list = ["Home", "Work", "School", "Med", "Shop", "Social", "Transport", "Meals", "Other"]
    dist_by_purp = np.zeros(9)
    #FUNCTION FOR ROOMS AND VEHICLES
    [hh_mem_i, av_veh_i, checks] = hh_details_set(ACS_tract_df, BTS_tract_df, checks)
    # FUNCTION FOR ESTABLISHING VEHICLE TRIPS
    [vtrp_i, dist_arr] = hh_vtrp_set(BTS_tract_df, hh_mem_i, av_veh_i, nan_check)
    dist_ind = [i for i in range(len(dist_arr))]

    # Iterate for number of days annually
    for day in range(0, 367):
        # Scale Function
        [wkday_scale, month_scale] = temp_scaling(day)
        start_point = "Home"
        # Iterate by number of vehicle trips per household
        for x in range(int(round(vtrp_i))):
            # Determine trip purpose by weekend or weekday weighted percentages
            wknd_test = day/7 % 1
            if wknd_test >= 0.714:
                # Weekend Vehicle Trip Purpose by weight (NHTS 2017 Trip Purpose Summary)
                vtrp_purp_pct = [35.04, 6.83, 5.57, 0.47, 24.98, 11.25,
                                 5.19, 9.84, 0.83]
            else:
                # Weekday Vehicle Trip Purpose by weight (NHTS 2017 Trip Purpose Summary)
                vtrp_purp_pct = [34.04, 19.84, 2.7, 1.68, 16.62, 6.28,
                                 10.97, 6.78, 1.09]

            [vtrp_dist_x, purp_x, start_time_x, start_point, home_hourly_dist, track_purpose] = vtrp_distance(x, vtrp_i, day, dist_ind, dist_arr, vtrp_purp_pct, start_point, home_hourly_dist, track_purpose)
            # Apply Geo and Temp Scaling to Trip Distance
            vtrp_dist_x = vtrp_dist_x*ug_scale*wkday_scale*month_scale
            # Add trip distance to total household hourly distance
            hh_hourly_dist[start_time_x[0]] = hh_hourly_dist[start_time_x[0]]+vtrp_dist_x
            trip_idx = purp_list.index(purp_x)
            dist_by_purp[trip_idx] = dist_by_purp[trip_idx] + vtrp_dist_x

            # Adjusting to Annual Hour
            s_t = start_time_x[0]
            s_h = day*24 + s_t
            #ann_hourly_dist[s_h] = tract_hourly_dist[s_t]
            ann_hourly_dist[s_h] = ann_hourly_dist[s_h] + vtrp_dist_x

            # CALCULATE THIS LATER, ELEMENT BY ELEMENT
#            ann_hourly_energy[s_h] = ann_hourly_energy[s_h] + ev_pct/100*ldv_rate*vtrp_dist_x

    return [ann_hourly_dist, checks, track_purpose, dist_by_purp]
