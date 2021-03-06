def trip_purpose(purp_x, track_purpose):
    if purp_x == "Home":
        # Vehicle Work-Trip Start Time by weight (NHTS 2017 Trip Start Times)
        start_time_pct = [0.65, 0.45, 0.22, 0.08, 0.12, 0.32, 1.08, 2.96, 2.57,
                          2.62, 3.85, 4.94, 6.20, 5.28, 6.10, 8.99, 10.95,
                          12.74, 8.75, 6.97, 5.33, 4.40, 2.71, 1.72]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        # Vehicle Work-Trip Distance by weight (NHTS 2017 Trip Distance)
        vtrp_dist_pct = [3.3, 14.9, 13.9, 9.9, 8.4, 6.2, 18.1, 9.0, 5.4, 5.6, 5.2]
        long_dist_metrics = [0.32, 79.84]#129.18
        track_purpose[0] += 1
    elif purp_x == "Work":
        start_time_pct = [0.03, 0.00, 0.00, 0.06, 2.32, 6.16, 14.61, 21.76,
                          12.74, 6.45, 4.42, 4.13, 6.89, 5.88, 4.16, 3.14, 2.60,
                          2.03, 0.95, 0.38, 0.38, 0.57, 0.32, 0.06]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [2.6, 10, 9.3, 7.6, 6.3, 6.0, 19.6, 13.4, 8.2, 9.4, 7.3]
        long_dist_metrics = [0.3, 72.87]#115.24
        track_purpose[1] += 1
    elif purp_x == "School":
        start_time_pct = [0, 0, 0, 0, 0.15, 0.77, 4.78, 13.73, 14.97, 14.66,
                          10.03, 4.78, 3.55, 3.86, 2.78, 2.01, 5.09, 7.10,
                          7.72, 2.16, 0.77, 0.46, 0.31, 0.00]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [3.2, 13, 12, 9.7, 8.8, 6.3, 19.3, 11.7, 4.9, 6.6, 4.4]
        long_dist_metrics = [0.29, 61.55]#92.6
        track_purpose[2] += 1
    elif purp_x == "Med":
        start_time_pct = [0, 0, 0, 0, 0.38, 0.38, 1.92, 7.31, 11.54, 17.69,
                          11.15, 6.54, 7.69, 9.62, 8.85, 8.08, 3.85, 1.54,
                          1.15, 0.385, 0.77, 0.385, 0, 0]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [2.9, 9.5, 11.8, 8.2, 8, 7.5, 21.1, 11.3, 7.4, 6.2, 6.2]
        long_dist_metrics = [0.25, 51.3]#72.1
        track_purpose[3] += 1
    elif purp_x == "Shop":
        start_time_pct = [0.141, 0, 0, 0, 0.057, 0.311, 1.102, 2.402, 4.747,
                          7.799, 11.02, 10.455, 9.749, 8.76, 8.223, 8.11, 7.827,
                          6.782, 5.397, 3.334, 1.978, 1.045, 0.537, 0.198]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [8.8, 21.7, 17.7, 11.3, 7.8, 5.7, 13.2, 6.1, 3, 2.4, 2.8]
        long_dist_metrics = [0.3, 106.89]#183.28
        track_purpose[4] += 1
    elif purp_x == "Social":
        start_time_pct = [0.07, 0.07, 0.07, 0, 0.49, 1.34, 1.9, 3.87, 5.41,
                          6.04, 6.61, 7.38, 5.62, 6.32, 7.1, 7.1, 8.36, 10.33,
                          9.7, 5.55, 3.16, 1.83, 1.12, 0.63]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [3.4, 12.9, 12.1, 10.3, 8.2, 5.8, 18.6, 8.9, 5.7, 5.4, 8.7]
        long_dist_metrics = [0.29, 97.06]#163.6
        track_purpose[5] += 1
    elif purp_x == "Transport":
        start_time_pct = [0.17, 0.17, 0.06, 0, 0.5, 0.94, 4.98, 21.76, 7.03,
                          3.1, 3.16, 3.27, 3.21, 4.04, 8.53, 11.68, 8.97, 8.19,
                          3.77, 2.05, 1.72, 1.61, 0.72, 0.33]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [5, 19.5, 15.8, 11.3, 7.6, 6.5, 16.2, 7.5, 4.1, 3.3, 3.1]
        long_dist_metrics = [0.32, 80.06]#129.62
        track_purpose[6] += 1
    elif purp_x == "Meals":
        start_time_pct = [0.21, 0.07, 0, 0, 0.35, 0.84, 2.31, 4.20, 4.20,
                          4.48, 5.46, 12.25, 14.36, 7.42, 5.74, 4.48, 4.9,
                          7.84, 8.75, 5.81, 3.57, 1.68, 0.84, 0.21]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [7.3, 21.4, 17.6, 11.5, 7.9, 6.3, 13.4, 5.6, 3, 3.2, 2.9]
        long_dist_metrics = [0.32, 126.01]#221.52
        track_purpose[7] += 1
    elif purp_x == "Other":
        start_time_pct = [0, 0, 0, 0, 0.51, 2.05, 3.59, 7.18, 8.72, 9.74,
                          8.72, 7.69, 7.69, 7.69, 5.13, 6.67, 5.64, 7.69, 4.62,
                          2.56, 2.05, 0.51, 0.51, 0.51]
        start_time_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          16, 17, 18, 19, 20, 21, 22, 23]
        vtrp_dist_pct = [4.4, 13, 11.3, 9.9, 6.4, 5.6, 21, 9.9, 5.4, 5.4, 7.7]
        long_dist_metrics = [0.26, 71.48]#112.46
        track_purpose[8] += 1

    return [start_time_pct, start_time_ind, vtrp_dist_pct, long_dist_metrics, track_purpose]
