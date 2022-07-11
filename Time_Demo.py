from time import *
from threading import Timer
from turtle import update



# print("start")
hours = 0
minutes = 59
seconds = 55
military=True

def print_timer(hours, minutes, seconds):
    # print("print timer")
    if military==False:
        if hours>12:
            hours=hours-12
            period = " PM"
        elif hours==12:
            period = " PM"
        else:
            if hours==0:
                hours=12
            period = " AM"
    else:
        period = ""

    if hours==0 and military==True:
        hours=f"0{str(hours)}"
    else:
        hours=f"{str(hours)}"

    if len(str(minutes))<2:
        minutes=f"0{str(minutes)}"
    else:
        minutes=f"{str(minutes)}"

    if len(str(seconds))<2:
        seconds=f"0{str(seconds)}"
    else:
        seconds=f"{str(seconds)}"

    output = f"{hours}:{minutes}:{seconds}{period}"
    print(output)


def update_timer():
    # print("update timer")
    global seconds
    global minutes
    global hours


    seconds +=1
    if seconds>=60:
        seconds=0
        minutes+=1
    
    if minutes>=60:
        hours+=1
        minutes=0

    if hours>=24:
        hours=0

    print_timer(hours,minutes,seconds)

    timer=Timer(1.0,update_timer)
    timer.start()
    # update_timer()

print_timer(hours,minutes,seconds)
t=Timer(1.0,update_timer)
t.start()





