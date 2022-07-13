from time import *
from threading import Timer as Thread

class Stopwatch:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.pause = False
        self.show_output = True

    def start_stopwatch(self):
        self.get_time()
        pass_time=Thread(1.0,self.update_stopwatch)
        pass_time.start()

    def reset_stopwatch(self):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.pause = False
        self.show_output=False

    def pause(self):
        self.pause=True

    def unpause(self):
        self.pause=False

    def get_time(self):
        # print("print stopwatch")
        h_display = self.hours
        m_display = self.minutes
        s_display = self.seconds

        if self.hours>0:
            h_display=f"{str(h_display)}:"
        else:
            h_display=""


        if self.minutes>=10:
            m_display=f"{str(m_display)}:"
        elif m_display>0 and self.hours>0:
            m_display=f"0{str(m_display)}:"
        else:
            m_display=""

        if self.seconds>=10:
            s_display=f"{str(s_display)}:"
        elif self.seconds>0 and self.minutes>0:
            s_display=f"0{str(s_display)}:"
        else:
            s_display=""

        output = f"{h_display}{m_display}{s_display}"
        print(output)


    def update_stopwatch(self):
        # print("update stopwatch")

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

        pass_time=Thread(1.0,self.update_stopwatch)
        pass_time.start()

    
    def change_stopwatch(self, hours, minutes, seconds):
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


asdf=Stopwatch()
asdf.start_stopwatch()

