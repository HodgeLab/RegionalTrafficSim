import numpy as np
def home_chg(ann_hourly_energy, ann_hourly_home_energy, home_hourly_dist, day, surp_energy, surp_charge, chargeLevel, av_veh_i, checks):
    hometrip_hour = []
    htrip_energy = []
    hr_full_chg = []
    ext_chg = []
    charge_duration = []
    charge_per_hour = np.zeros(24)
    additional_rate = []
    hour_at_c = []
    y = 0
    if chargeLevel == "L1":
        # Level 1 Charge Rate
        c_rate = 1.4
    elif chargeLevel == "L2":
        # Level 2 Charge Rate
        c_rate = 7.6

    # Include previous day's leftover charging
    if sum(surp_charge) > 0:
        charge_per_hour = surp_charge
        surp_charge = np.zeros(24)

    # Calculate daily energy per household
    daily_hh_energy = sum(ann_hourly_energy[day*24:(day+1)*24])

    for x in range(0, 24):
        if home_hourly_dist[day*24+x] > 0:
            hometrip_hour.append(x)
            htrip_energy.append(sum(ann_hourly_energy[(day*24)+y:(day*24)+(x+1)]) + surp_energy)
            surp_energy = 0
            y = x+1

    if sum(ann_hourly_energy[day*24+y:(day+1)*24]) > 0:
        surp_energy = sum(ann_hourly_energy[day*24+y:(day+1)*24])
    else:
        surp_energy = 0
    # Calc hours of full charge and partial charge
    for n in range(0, np.size(hometrip_hour)):
        hr_full_chg.append(int(htrip_energy[n]/c_rate))
        ext_chg.append(htrip_energy[n]/c_rate % 1)
        additional_rate.append(1)
        hour_at_c.append(0)
        # Determine duration of charge
        if ext_chg[n] > 0:
            charge_duration.append(hr_full_chg[n] + 1)
        else:
            charge_duration.append(hr_full_chg[n])

        if hometrip_hour[n] + charge_duration[n] >= 48:
            if av_veh_i <= 1:
                checks[3] += 1
            charge_duration[n] = charge_duration[n]/2
            hr_full_chg[n] = hr_full_chg[n]/2
            additional_rate[n] = 2
            if hr_full_chg[n] % 1 > 0:
                hour_at_c[n] = 1
            else:
                charge_duration[n] = charge_duration[n] + 1
            charge_duration[n] = int(charge_duration[n])
            hr_full_chg[n] = int(hr_full_chg[n])
        for x in range(hometrip_hour[n], hometrip_hour[n]+charge_duration[n]):
            if x < hometrip_hour[n] + hr_full_chg[n]:
                if x >= 24:
                    j = x - 24
                    surp_charge[j] = surp_charge[j] + c_rate*additional_rate[n]
                else:
                    charge_per_hour[x] = charge_per_hour[x] + c_rate*additional_rate[n]
            else:
                if x >= 24:
                    j = x - 24
                    surp_charge[j] = surp_charge[j] + c_rate*ext_chg[n] + c_rate*hour_at_c[n]
                else:
                    charge_per_hour[x] = charge_per_hour[x] + c_rate*ext_chg[n] + c_rate*hour_at_c[n]

                ann_hourly_home_energy[day*24:(day+1)*24] = charge_per_hour
                if day == 366 and n == np.size(hometrip_hour)-1:
                    ann_hourly_home_energy[0:24] = ann_hourly_home_energy[0:24] + surp_charge
                    if surp_energy > 0:
                        lst_chg = int(surp_energy/c_rate)
                        lst_ext_chg = surp_energy/c_rate % 1
                        if lst_ext_chg > 0:
                            lst_duration = lst_chg + 1
                            for n in range(lst_duration-1):
                                ann_hourly_home_energy[8807-(lst_duration-n)] = ann_hourly_home_energy[8807-(lst_duration-n)] + c_rate
                            ann_hourly_home_energy[8807] = ann_hourly_home_energy[8807] + lst_ext_chg*c_rate
                        else:
                            lst_duration = lst_chg
                            for n in range(lst_duration-1):
                                ann_hourly_home_energy[8807-(lst_duration-n)] = ann_hourly_home_energy[8807-(lst_duration-n)] + c_rate
                        surp_energy = 0
                    surp_charge = np.zeros(24)
    # if abs(sum(ann_hourly_energy) - sum(ann_hourly_home_energy) - surp_energy - sum(surp_charge)) > 0.5:
    #     print("End-of-day mismatch")
    #     print("Charge Duration: ", charge_duration)
    #     print("hometrip hours: ", hometrip_hour)
    #     print("surp_charge: ", surp_charge, "sum: ", sum(surp_charge))
    #     print("charge per hour: ", charge_per_hour, "sum: ", sum(charge_per_hour))
    #     print("surp_energy: ", surp_energy)
    #     print("daily energy: ", daily_hh_energy)
    #     breakpoint()
    return (surp_energy, surp_charge, ann_hourly_home_energy, checks)
