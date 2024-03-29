import sys
def set_paths(source):
    # Set directories
    if source == "Surf":
        sys.path.append(r"C:\Users\antho\github\RegionalTrafficSim\trip_count")
        sys.path.append(r"C:\Users\antho\github\RegionalTrafficSim\vmt_calc")
        home_dir = r"C:\Users\antho\github\RegionalTrafficSim"
        data_dir = r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database"
        output_dir = r"C:\Users\antho\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database\ABM_Outputs\Ext_Tracts"
    elif source =="SEEC":
        sys.path.append(r"C:\Users\A.J. Sauter\github\RegionalTrafficSim\trip_count")
        sys.path.append(r"C:\Users\A.J. Sauter\github\RegionalTrafficSim\vmt_calc")
        home_dir = r"C:\Users\A.J. Sauter\github\RegionalTrafficSim"
        data_dir = r"C:\Users\A.J. Sauter\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database"
        output_dir = r"C:\Users\A.J. Sauter\OneDrive - UCB-O365\Active Research\ASPIRE\CoSimulation Project\Texas Traffic Data\NHTS_Database\ABM_Outputs\Ext_Tracts"
    elif source == "Alpine":
        sys.path.append(r"/home/ansa1773/sts_scripts/trip_count")
        sys.path.append(r"/home/ansa1773/sts_scripts/vmt_calc")
        home_dir = r"/home/ansa1773/sts_scripts"
        data_dir = r"/scratch/alpine/ansa1773/STS_Model"
        output_dir = r"/scratch/alpine/ansa1773/STS_Model/ABM_Outputs"
    elif source == "Summit":
        sys.path.append(r"/home/ansa1773/sts_scripts/trip_count")
        sys.path.append(r"/home/ansa1773/sts_scripts/vmt_calc")
        home_dir = r"/home/ansa1773/sts_scripts"
        data_dir = r"/scratch/summit/ansa1773/STS_Model"
        output_dir = r"/scratch/summit/ansa1773/STS_Model/ABM_Outputs"

    return [home_dir, data_dir, output_dir]
