def vacancy_check(ACS_tract_df, ACS_df, BTS_df, checks, tot_tracts, hh_room_cnt, hh_cnt, g):
    #print("Values for: " + str(tot_tracts[g]) + " DO NOT EXIST")
    bad_index = ACS_tract_df.index
    bad_index = bad_index[0]
    good_index = bad_index-1
    ACS_tract_df = ACS_df[good_index:bad_index]
    new_id = ACS_tract_df['tract_id'].values[0]
    new_loc = ACS_tract_df['Geographic Area Name'].values[0]
    hh_room_cnt = ACS_tract_df["est_tot_rooms"].values[0]
    #print("Supplant with: " + str(new_id) + " located in: " + new_loc)
    checks[2] +=1

    BTS_tract_df = BTS_df[BTS_df["geocode"] == new_id]
    tot_pop = BTS_tract_df["tot_pop"].values[0]
    hh_cnt = BTS_tract_df["hh_cnt"].values[0]
        # Iterate by Households (samples) in each tract
    return [ACS_tract_df, hh_room_cnt, checks, BTS_tract_df, tot_pop, hh_cnt]
