from hh_distance import hh_distance
def tract_distance(g, tot_tracts, BTS_df, ACS_df):
    # Initialize tracking parameters
    tot_tract_hourly_dist = np.zeros(8808)
    tot_tract_hourly_energy = np.zeros(8808)
    tot_tract_h_hourly_energy = np.zeros(8808)
    # Initiate In-Home Charging parameters
    tot_tract_hourly_dist_chg = np.zeros(8808)
    tot_tract_hourly_chg = np.zeros(8808)
    daily_hometrip_pct = np.zeros(24)
    hourly_mi_chg = np.zeros(24)
    dist_per_hour = np.zeros(24)

    # Retrieve tract-specific datasets
    BTS_tract_df = BTS_df[BTS_df["geocode"] == tot_tracts[g]]
    ACS_tract_df = ACS_df[ACS_df["tract_id"] == tot_tracts[g]]
    # Pull tract population and household counts
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

    # Subroutine that ensures non-zero room and household counts
    [ACS_tract_df, new_id, new_loc, hh_room_cnt, BTS_tract_df, tot_pop, hh_cnt] =
        vacancy_check(ACS_tract_df, ACS_df, BTS_df, tot_tracts, hh_room_cnt, hh_cnt, g)
    nan_check = np.isnan(np.sum(BTS_tract_df.values[0]))

for hh in hh_cnt:
    hh_distance(hh, ACS_tract_df, BTS_tract_df)
