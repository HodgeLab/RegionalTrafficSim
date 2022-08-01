from hh_details_set import hh_details_set
#from vtrp_distance import vtrp_distance
from temp_scaling import temp_scaling
from hh_vtrp_set import hh_vtrp_set
import numpy as np
import pandas as pd
def hh_distance_tc(ACS_tract_df, BTS_tract_df, ug_scale, nan_check, checks):

    #FUNCTION FOR ROOMS AND VEHICLES
    [hh_mem_i, av_veh_i, checks] = hh_details_set(ACS_tract_df, BTS_tract_df, checks)
    # FUNCTION FOR ESTABLISHING VEHICLE TRIPS
    [vtrp_i, dist_arr] = hh_vtrp_set(BTS_tract_df, hh_mem_i, av_veh_i, nan_check)

    return [checks, vtrp_i]
