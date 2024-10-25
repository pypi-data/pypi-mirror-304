from .TimeCalcModule import *
import datetime

def minMax(morning, mid, midend):
        check = [morning, mid, midend]
        for test in check:
            if not validateTime(test):
                return False
        morningTime = validateTime(mid) - validateTime(morning)
        workTimes=[492,540]
        dayFinish=[]
        for minmax in workTimes:
            workHours = minmax - morningTime
            workHours += validateTime(midend)
            workHours = convertMinutes(workHours)
            dayFinish.append(workHours)
        return dayFinish

def time_until_end(end):
    now = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M")
    seconds = int(datetime.datetime.strftime(datetime.datetime.now(), "%S"))
    now_min = validateTime(now)
    end_min = validateTime(end)
    timediff_min = end_min - now_min
    yeeees= convertMinutes(timediff_min)
    totalt_time= f"{yeeees[0]:02}:{yeeees[1]:02}"
    return totalt_time, timediff_min
