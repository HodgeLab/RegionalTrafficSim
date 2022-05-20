def data_gather(data_dir):
    import os
    import pandas as pd
    # ALL RELEVANT DATAFRAMES
    # If any of these do not exist, throw an error
    # Retrieve load names list
    os.chdir(data_dir)
    og_load_list = pd.read_excel("Load_List.xlsx")["Load_Names"].tolist()

    # Retrieve dataframes from both BTS LATCH and ACS 5-Year Reports
    ACS_df = pd.read_excel("ACS_5Y_2016.DP04_Tx_Tracts.xlsx")
    BTS_df = pd.read_excel("BTS_LatchB_Pop_NumDailyTrips.xlsx")
    links_df = pd.read_excel("Load_Tract_Linkages.xlsx")

    # IF THIS SPREADSHEET DOES NOT EXIST, CREATE FUNCTION FOR THAT PROCESS
    tract_by_county_df = pd.read_excel("Tracts_By_County.xlsx")
    # Retrieve dataframe for geocodes (tracts for each bus)
    geo_df = pd.read_excel("bus_load_blocks.xlsx")

    return [og_load_list, ACS_df, BTS_df, links_df, tract_by_county_df, geo_df]

if __name__ == "__data_gather__":
    data_gather()