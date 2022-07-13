from time import *
from threading import Timer as Thread



class Clock:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.military = False
        self.pause = False
        self.show_output = True

    def start_clock(self):
        self.get_time()
        pass_time=Thread(1.0,self.update_clock)
        pass_time.start()

    def reset_clock(self):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.military = False
        self.pause = False
        self.show_output=False

    def pause(self):
        self.pause=True

    def unpause(self):
        self.pause=False

    def get_time(self):
        # print("print timer")
        h_display = self.hours
        m_display = self.minutes
        s_display = self.seconds


        if self.military==False:
            if self.hours>12:
                h_display=self.hours-12
                period = " PM"
            elif self.hours==12:
                period = " PM"
            else:
                if self.hours==0:
                    h_display=12
                period = " AM"
        else:
            
            period = ""

        if h_display==0 and self.military==True:
            h_display=f"0{str(h_display)}"
        else:
            h_display=f"{str(h_display)}"

        if len(str(m_display))<2:
            m_display=f"0{str(m_display)}"
        else:
            m_display=f"{str(m_display)}"

        if len(str(s_display))<2:
            s_display=f"0{str(s_display)}"
        else:
            s_display=f"{str(s_display)}"

        output = f"{h_display}:{m_display}:{s_display}{period}"
        print(output)


    def update_clock(self):
        # print("update timer")

        if self.pause==False:
            self.seconds +=1
            if self.seconds>=60:
                self.seconds=0
                self.minutes+=1
            
            if self.minutes>=60:
                self.hours+=1
                self.minutes=0

            if self.hours>=24:
                self.hours=0

        if self.show_output==True:
            self.get_time()

        pass_time=Thread(1.0,self.update_clock)
        pass_time.start()

    
    def change_clock(self, hours, minutes, seconds):
        if self.seconds>=60:
            self.seconds=0
        else:
            self.seconds = seconds
        
        if self.minutes>=60:
            self.minutes=0
        else:
            self.minutes = minutes

        if self.hours>=24:
            self.hours=0
        else:
            self.hours = hours


asdf=Clock()
asdf.start_clock()

