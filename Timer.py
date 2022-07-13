from time import *
from threading import Timer as Thread



class timer:
    def __init__(self, hours=0, minutes=5, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.pause = False
        self.show_output = True

    def start_timer(self):
        self.get_time()
        pass_time=Thread(1.0,self.update_timer)
        pass_time.start()

    def reset_timer(self):
        self.hours = 0
        self.minutes = 5
        self.seconds = 0
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



        h_display=f"{str(h_display)}"

        if len(str(m_display))<2:
            m_display=f"0{str(m_display)}"
        else:
            m_display=f"{str(m_display)}"

        if len(str(s_display))<2:
            s_display=f"0{str(s_display)}"
        else:
            s_display=f"{str(s_display)}"

        output = f"{h_display}:{m_display}:{s_display}"
        print(output)


    def update_timer(self):
        # print("update timer")

        if self.pause==False:
            self.seconds-=1
            if self.seconds<0:
                self.minutes-=1
                if self.minutes<0:
                    self.hours-=1
                    if self.hours<0:
                        return self.Timer_Done()
                    self.minutes=59
                self.seconds=59 


        if self.show_output==True:
            self.get_time()

        pass_time=Thread(1.0,self.update_timer)
        pass_time.start()


    def Timer_Done(self):
        pass
    
    def change_timer(self, hours, minutes, seconds):
        if self.seconds>=60:
            self.seconds=60
        else:
            self.seconds = seconds
        
        if self.minutes>=60:
            self.minutes=60
        else:
            self.minutes = minutes

        self.hours = hours


asdf=timer()
asdf.start_timer()

