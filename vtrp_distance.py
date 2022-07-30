import random
import numpy as np
from trip_purpose import trip_purpose
from scipy.stats import genhyperbolic
def vtrp_distance(x, vtrp_i, day, dist_ind, dist_arr, vtrp_purp_pct, start_point, home_hourly_dist, track_purpose, checks):
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
    [start_time_pct, start_time_ind, vtrp_dist_pct, gh_dist_metrics, track_purpose] = trip_purpose(purp_x, track_purpose)
    # Calculate trip start time, distance range, and distance
    start_time_x = random.choices(start_time_ind, weights = start_time_pct, k=1)
    dist_range = random.choices(dist_ind, weights = vtrp_dist_pct, k=1)
    #dist_arr[10][1] = long_dist_metrics[0]
    dist_range = dist_range[0]
    # First and last distance range require non-uniform distribution
    if dist_range == 0:
        dist_check = 0
        # Reroll hyperbolic function until vtrip is within bounds (less than 0.5 mi)
        while dist_check <= 0 or dist_check > 0.5:
            vtrp_dist_x = genhyperbolic.rvs(1, 1, 0, loc=gh_dist_metrics[0], scale=0.125) # CHANGE LOC ACCORDINGLY
            dist_check = vtrp_dist_x
    elif dist_range == 10:
        dist_check = 0
        # Reroll hyperbolic function until vtrp is within bounds (above 30.5 mi)
        while dist_check < 30.5:
            vtrp_dist_x = genhyperbolic.rvs(2, 0.75, 0, loc=gh_dist_metrics[1], scale=11.77) # CHANGE LOC ACCORDINGLY
            dist_check = vtrp_dist_x
    # All mid-range distances are derived from bounded uniform distributions
    else:
        vtrp_dist_x = (dist_arr[dist_range][1]-dist_arr[dist_range][0])*random.uniform(0, 1) + dist_arr[dist_range][0]
        checks[0] +=1
    if purp_x == "Home":
        s_t = start_time_x[0]
        s_h = day*24 + s_t
        # Track ONLY home trip distance (for use in home charging scenarios)
        home_hourly_dist[s_h] = home_hourly_dist[s_h] + 1

    return [vtrp_dist_x, purp_x, start_time_x, start_point, home_hourly_dist, track_purpose, checks]
