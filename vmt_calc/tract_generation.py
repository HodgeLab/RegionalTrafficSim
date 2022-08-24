def tract_generation(og_load_list, geo_df, tract_by_county_df):
    # Initialize geocode and load lists
    geocode = []
    dup_list = []
    load_list = []
    geo_dup_list = []
    tot_geo_list = []
    # Create list of tracts without duplicates
    for i in range(len(og_load_list)):
        loadsplit = og_load_list[i].split('.')
        load_list.append(loadsplit[0])
        geo_load_df = geo_df[geo_df["load_name"] == load_list[i]]
        tract_id = geo_load_df["tract"].values[0]
        tot_geo_list.append(tract_id)
        if tract_id not in geocode:
            geocode.append(tract_id)
        else:
            dup_list.append(load_list[i])
            geo_dup_list.append(tract_id)
    # Create a list of all remaining tracts within ERCOT's jurisdiction
    ERCOT_tracts = tract_by_county_df["tract_name"]
    my_tracts = []
    for i in range(len(ERCOT_tracts)):
        tract_id = ERCOT_tracts[i]
        if tract_id not in geocode:
            my_tracts.append(tract_id)
    tot_tracts = geocode + my_tracts
    return [tot_tracts]
