def validateTime(time):
    valTime=[]
    if ":" in time or "," in time or "." in time:
        time=time.replace(" ",":").replace(",",":").replace(".",":")
        valTime=time.split(":")
    elif len(time) == 3 or len(time) == 4:
            valTime.append(time[:-2])
            valTime.append(time[-2:])
    else:
        return False
    if valTime[0].isdigit() and valTime[1].isdigit():
        valTime[0]=int(valTime[0])
        valTime[1]=int(valTime[1])
    else:
        return False
    if valTime[0] >23 or valTime[1] >59:
        return False
    minuteTime=valTime[0]*60+valTime[1]
    return minuteTime

def convertMinutes(totalMinutes):
    overspill = totalMinutes % 60
    hour = (totalMinutes - overspill) / 60
    return int(hour),overspill