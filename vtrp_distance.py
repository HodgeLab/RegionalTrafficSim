import random
import numpy as np
from trip_purpose import trip_purpose
def vtrp_distance(x, vtrp_i, day, dist_ind, dist_arr, vtrp_purp_pct, start_point, home_hourly_dist, track_purpose):
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

    # Determine weights based on trip purpose
    [start_time_pct, start_time_ind, vtrp_dist_pct, long_dist_cap, track_purpose] = trip_purpose(purp_x, track_purpose)
    # Calculate trip start time, distance range, and distance
    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
    dist_arr[10][1] = long_dist_cap
    dist_range = dist_range[0]
    vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0])*random.random() + dist_arr[dist_range][0]

    if purp_x == "Home":
        s_t = start_time_x[0]
        s_h = day*24 + s_t
        # Track ONLY home trip distance (for use in home charging scenarios)
        home_hourly_dist[s_h] = home_hourly_dist[s_h] + 1

    return [vtrp_dist_x, purp_x, start_time_x, start_point, home_hourly_dist, track_purpose]
