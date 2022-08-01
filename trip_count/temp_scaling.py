def temp_scaling(day):
    # Temporal Scaling
    # Determine this hour's percentage of one total week
    wknd = day/168 % 1
    # Decide if the hour is on a weekday or a weekend
    if wknd >= 0.714:
        wkday_scale = 1.181 # 18.1% Increase in Drive Length for Weekends
    else:
        wkday_scale = 0.9411 # 5.9% Decrease in Drive Length for Weekdays
    # Determine current day of the year
    day_chk = day/24
    if day_chk <= 31: #January
        month_scale = 0.852
    elif day_chk <= 59: #February
        month_scale = 1.095
    elif day_chk <= 90: #March
        month_scale = 0.945
    elif day_chk <= 120: #April
        month_scale = 1.114
    elif day_chk <= 151: #May
        month_scale = 0.974
    elif day_chk <= 181: #June
        month_scale = 0.995
    elif day_chk <= 212: #July
        month_scale = 1.132
    elif day_chk <= 243: #August
        month_scale = 0.909
    elif day_chk <= 273: #September
        month_scale = 1.062
    elif day_chk <= 304: #October
        month_scale = 0.922
    elif day_chk <= 334: #November
        month_scale = 1.056
    elif day_chk <= 365: #December
        month_scale = 0.962
    else: # January Again (For the Forecast Window)
        month_scale = 0.852

    return [wkday_scale, month_scale]
