##############################################################################################################
# This is the GUI Base, this is the center of all of the code. Everything else that happens stems from this
# Almost Everything here was coded Ethan with minor modifications by Matthew and Zach
##############################################################################################################

# Here is where we import all the modules for the program
from tkinter import *
import RPi.GPIO as GPIO
from random import *
from math import *
from Keypad import *
from The_Button import *
from Wires import *
from targeting import *;
from time import *
from lights import *
from targeting import *
from morse import *
import pygame


# This is the main GUI

class MainGUI(Frame):
    def __init__(self, parent):
        # Here we inherit all the tkinter Frame functions to be used in the rest of the program
        Frame.__init__(self, parent, bg="white")
        # Here we setg the program to open in full screen and to show no cursor on the raspberry pi
        parent.attributes("-fullscreen", True)
        self.config(cursor="none")
        # Here we set up pygame for the music
        pygame.mixer.init()
        pygame.mixer.set_num_channels(10)

        # Here we set up some variable for the rest of the function
        self.rows=1
        self.cols=1
        self.pack(fill=BOTH, expand=True)
        self.reset()

    # function for sending output to the pins 
    # seems that output must be sent through the Frame object or it halts
    def pinOutput (self, pin, signal):
        GPIO.output(pin, signal);
        return;
    
    # In order to save space in the init and also to allow for easy and clean reseting when the user starts over, we store all the class variable
    # and other set up resourses in the reset function
    def reset(self):
        try:
            GPIO.cleanup()
        except:
            pass
        self.music_playing = False
        self.Alive = True

        # this is the number of mistakes the user can 
        self.maxstrikes = 2
        self.strikes = 0

        # This is how much time the defuser gets to defuse the bomb
        self.startmins = IntVar()
        self.startsecs = IntVar()
        self.startmins = 10
        self.startsecs = 0
        self.timer_pause = False
        self.timer = None
        self.mins = IntVar()
        self.secs = IntVar()
        self.time = StringVar()
        self.mins = self.startmins
        self.secs = self.startsecs
        if self.mins < 10:
            if self.secs < 10:
                self.time.set(f"0{self.mins}:0{ceil(self.secs)}")
            else:
                self.time.set(f"0{self.mins}:{ceil(self.secs)}")
        else:
            if self.secs < 10:
                self.time.set(f"{self.mins}:0{ceil(self.secs)}")
            else:
                self.time.set(f"{self.mins}:{ceil(self.secs)}")

        
        self.hp = StringVar()
        self.hp.set("[{}{}]".format("X"*self.strikes, " "*(self.maxstrikes-self.strikes)))
        self.loc = "Home"
        self.current_module = None
        self.counter = None

        # Here we store the Started and Done state of each module
        self.Module_1_Started = False
        self.Module_2_Started = False
        self.Module_3_Started = False
        self.Module_4_Started = False
        self.Module_5_Started = False
        self.Module_6_Started = False
        self.Module_1_Done = False
        self.Module_2_Done = False
        self.Module_3_Done = False
        self.Module_4_Done = False
        self.Module_5_Done = False
        self.Module_6_Done = False
        self.Modules_Done = [self.Module_1_Done, self.Module_2_Done, self.Module_3_Done, self.Module_4_Done, self.Module_5_Done, self.Module_6_Done]

        # Accessors and Mutators
        @property
        def timer_pause(self):
            return self._timer_pause
        @timer_pause.setter
        def timer_pause(self, value):
            self._timer_pause = value

        @property
        def maxstrikes(self):
            return self._maxstrikes
        @maxstrikes.setter
        def maxstrikes(self, value):
            self._maxstrikes = value

        @property
        def startmins(self):
            return self._startmins
        @startmins.setter
        def startmins(self, value):
            self._startmins = value
        
        @property
        def startsecs(self):
            return self._startsecs
        @startsecs.setter
        def startsecs(self, value):
            self._startsecs = value
        
        @property
        def mins(self):
            return self._mins
        @mins.setter
        def mins(self, value):
            self._mins = value
        
        @property
        def secs(self):
            return self._secs
        @secs.setter
        def secs(self, value):
            self._secs = value
        
        @property
        def strikes(self):
            return self._strikes
        @strikes.setter
        def strikes(self, value):
            self._strikes = value
        
        @property
        def loc(self):
            return self._loc
        @loc.setter
        def loc(self, value):
            self._locs = value
        
        @property
        def counter(self):
            return self._counter
        @counter.setter
        def counter(self, value):
            self._counter = value
        
        @property
        def rows(self):
            return self._rows
        @rows.setter
        def rows(self, value):
            self._rows = value
        
        @property
        def cols(self):
            return self._cols
        @cols.setter
        def cols(self, value):
            self._cols = value

        # Here we set each of the 6 modules
        # The modules could be randomized or set to None to not in the game.
        self.Module_1 = Module_The_Button(self, 22)
        self.Module_2 = Module_Keypad(self)
        self.Module_3 = Module_Wires(self)
        self.Module_4 = Module_Targeting(self)
        self.Module_5 = Module_Flashing_Lights(self)
        self.Module_6 = Module_Morse_Code(self)
        
        # Here we run the program for the start screen
        self.start_screen()

    def start_screen(self):
        # Heere we start music and have it loop
        pygame.mixer.music.load("music/wait.mp3")
        pygame.mixer.music.play(loops=-1)
        # Here we clear the GPIO board if its connected just in case
        try:
            GPIO.cleanup()
        except:
            pass
        
        # Here we clear the Frame with the clearFrame function and set up the rest of the interface
        # We do this in every screen
        self.clearFrame()
        self.rows = 2
        self.cols = 1
        self.loc = "Home"

        # These buttons allow you to either quit the program or start the game
        button = Button(self, bg="red", text="Push to Start", font=(
            "TexGyreAdventor", 25), borderwidth=10, activebackground="tomato", command=lambda: self.MainMenu())
        button.grid(row=0, column=0, sticky=N+S+E+W, padx=5, pady=5)

        quit = Button(self, bg="dim gray", text="Quit", font=("TexGyreAdventor", 25),
                      borderwidth=10, activebackground="light grey", command=lambda: self.quit())
        quit.grid(row=1, column=0, sticky=N+S+E+W, padx=5, pady=5)

        # Here we con figure the rows an coulmns, and pack. We do this in every screen
        Grid.rowconfigure(self, 0, weight=3)
        Grid.rowconfigure(self, 1, weight=1)

        Grid.columnconfigure(self, 0, weight=1)

        self.pack(fill=BOTH, expand=True)

    def MainMenu(self):
        # Here we run the function to play the main music for the game
        self.play_main_music()
        try:
            GPIO.cleanup()
        except:
            pass
    
        # Sut up
        self.clearFrame()
        self.loc="Home"
        self.rows = 4
        self.cols = 3

        # Here we set the current module (0 for Home) so that it the program is paused, it will resume.
        self.current_module = 0

        # Here we call a function for various predefined buttons
        # The first 4 will be called in almost every screen/module
        # The last 6 will be called for the main menu every time
        self.pause_button(0, 0, 3)
        self.countdown(1, 0, 1)
        self.location(1, 1, 1)
        self.health(1, 2, 1)
        self.Button1(2, 0, 1)
        self.Button2(2, 1, 1)
        self.Button3(2, 2, 1)
        self.Button4(3, 0, 1)
        self.Button5(3, 1, 1)
        self.Button6(3, 2, 1)

        # Here we test if each module has been completed if occupied
        try:
            self.Module_1_Done = self.Module_1.Module_Done
        except:
            self.Module_1_Done = True
        try:
            self.Module_2_Done = self.Module_2.Module_Done
        except:
            self.Module_2_Done = True
        try:
            self.Module_3_Done = self.Module_3.Module_Done
        except:
            self.Module_3_Done = True
        try:
            self.Module_4_Done = self.Module_4.Module_Done
        except:
            self.Module_4_Done = True
        try:
            self.Module_5_Done = self.Module_5.Module_Done
        except:
            self.Module_5_Done = True
        try:
            self.Module_6_Done = self.Module_6.Module_Done
        except:
            self.Module_6_Done = True

        # Configure Grid
        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=1)

        for row in range(2, self.rows):
            Grid.rowconfigure(self, row, weight=3)
        for col in range(self.cols):
            Grid.columnconfigure(self, col, weight=3)

        # Here is our win condition
        if (self.Module_1_Done==True and self.Module_2_Done==True and self.Module_3_Done==True and self.Module_4_Done==True and self.Module_5_Done==True and self.Module_6_Done==True):
            self.Game_Win()

        self.pack(fill=BOTH, expand=True)

    def play_main_music(self):
        # Here we set up the main music for the game and play it
        if self.music_playing == False:
            self.music_playing = True
            pygame.mixer.music.load("music/bomb_music.mp3")
            pygame.mixer.music.play(loops=-1)

    def pause_main_music(self):
        # Here we give the ability to pause the main music
        if self.music_playing == True:
            self.music_playing = False
            pygame.mixer.music.pause

    def clearFrame(self):
        # Clean up gpio
        try:
            GPIO.cleanup()
        except:
            pass
        if self.counter is not None:
            self.after_cancel(self.counter)
            self.counter = None
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()

        # Configure Grid
        for row in range(self.rows):
            Grid.rowconfigure(self, row, weight=0)
        for col in range(self.cols):
            Grid.columnconfigure(self, col, weight=0)

        self.pack_forget()
            
    def pause(self):
        # Music and setup
        self.pause_main_music()
        pygame.mixer.music.load("music/wait.mp3")
        pygame.mixer.music.play(loops=-1)
        self.clearFrame()
        self.rows = 3
        self.cols = 1

        # Here we set up the menu buttons for the menu
        resume = Button(self, bg="red", text="Resume", font=("TexGyreAdventor", 25), borderwidth=10, activebackground="blue", command=lambda: self.resume())
        resume.grid(row=0, column=0, sticky=N+S+E+W, padx=5, pady=5, columnspan=1)

        reset = Button(self, bg="green", text="Reset", font=("TexGyreAdventor", 25), borderwidth=10, activebackground="forest green", command=lambda: self.reset())
        reset.grid(row=1, column=0, sticky=N+S+E+W, padx=5, pady=5, columnspan=1)

        _quit = Button(self, bg="dim gray", text="Quit", font=("TexGyreAdventor", 25), borderwidth=10, activebackground="light grey", command=lambda: self.quit())
        _quit.grid(row=2, column=0, sticky=N+S+E+W, padx=5, pady=5, columnspan=1)

        # Cunfigure Grid
        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.rowconfigure(self, 2, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        self.pack(fill=BOTH, expand=True)

    def resume(self):

        # Here we look to see what the last module the user was in and then return to that module
        if self.current_module == 0:
            self.MainMenu()

        elif self.current_module == 1:
            self.Module_1.main(self.Module_1_Started)

        elif self.current_module == 2:
            self.Module_2.main(self.Module_2_Started)

        elif self.current_module == 3:
            self.Module_3.main(self.Module_3_Started)

        elif self.current_module == 4:
            self.Module_4.main(self.Module_4_Started)

        elif self.current_module == 5:
            self.Module_5.main(self.Module_5_Started)

        elif self.current_module == 6:
            self.Module_6.main(self.Module_6_Started)


    def update_timer(self):
        tick = 500
        if self.timer_pause==False:
            # Here we have the updater call it self and the pace of the updates depends on the number of strikes 
            if self.strikes == 0:
                self.counter = self.after(tick, self.update_timer)
            elif self.strikes == 1:
                self.counter = self.after(int((tick/4)*3), self.update_timer)
            elif self.strikes == 2:
                self.counter = self.after(int(tick/2), self.update_timer)
            else:
                self.counter = self.after(int(tick/2), self.update_timer)
            
            # Here we lower the timer by one second and if tick it over if needed
            self.secs -= (tick/1000)
            if self.secs < 0:
                self.secs = 59
                self.mins -= 1
                if self.mins < 0:
                    self.secs = 0
                    self.mins = 0
                    self.Game_Over()

            # We format the label for the timer widget
            if self.mins < 10:
                if ceil(self.secs) < 10:
                    self.time.set(f"0{self.mins}:0{ceil(self.secs)}")
                else:
                    self.time.set(f"0{self.mins}:{ceil(self.secs)}")
            else:
                if self.secs < 10:
                    self.time.set(f"{self.mins}:0{ceil(self.secs)}")
                else:
                    self.time.set(f"{self.mins}:{ceil(self.secs)}")

            # If the timer is below 30 seconds if flashes red and white to add suspense
            if (self.mins < 1) and (self.secs <= 30):
                if float(self.secs).is_integer()==False:
                    self.timer.config(fg="white")
                else:
                    self.timer.config(fg="red")
                    
            else:
                if self.Alive==True:
                    pass
            
            # Here we make a ticking noise every time the timer ticks down
            if float(self.secs).is_integer()==False:
                clock_tick = pygame.mixer.Sound("music/clock_tick.wav")
                clock_tick.play()
                
            
            
            self.update()

    def countdown(self, x, y, span):

        # Here we set up the count down widget and call the counter
        self.timer = Label(self, textvariable=self.time,
                      bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        self.timer.grid(row=x, column=y, sticky=N+S+E+W,
                   padx=5, pady=5, columnspan=span)
        if self.counter is None and self.Alive == True:
            self.counter = self.after(1000, self.update_timer)
        
    def strike(self):
        # Here we give the user a strike and check if the game needs to end
        self.strikes += 1
        self.hp.set("[{}{}]".format("X"*self.strikes, " "*(self.maxstrikes-self.strikes)))
        if self.strikes > self.maxstrikes:
            self.Game_Over()
        self.update()

    def health(self, x, y, span):
        # Here we to set up the health widget
        self.healthlabel = Label(self, textvariable=self.hp, bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        self.healthlabel.grid(row=x, column=y, sticky=N+S+E+W, padx=5,
                    pady=5, columnspan=span)

    def pause_button(self, x, y, span):
        # Here we set up the pause widget
        button = Button(self, bg="gray", text="Pause", font=("TexGyreAdventor", 25),
                        borderwidth=10, activebackground="light grey", command=lambda: self.pause())
        button.grid(row=x, column=y, sticky=N+S+E+W, pady=5, columnspan=span)

    def back_button(self, x, y, span):
        # Here we set up the back button widget
        back_button = Button(self, bg="gray", text="Back", font=("TexGyreAdventor", 25),
                             borderwidth=10, activebackground="light grey", command=lambda: self.MainMenu())
        back_button.grid(row=x, column=y, sticky=N+S+E+W, pady=5, columnspan=span)

    def location(self, x, y, span):
        # Here we set up the location widget
        location = Label(self, text=f"{self.loc}",
                         bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        location.grid(row=x, column=y, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=span)

    def Button1(self, x, y, span):
        # Here we set up the module
        try:
            # If the module is done we turn it green
            if self.Module_1.Module_Done == True:
                button_color = "lime green"
                background = "lime green"
            else:
                button_color = "tomato"
                background = "tomato"
        except:
            button_color = "tomato"
            background = "tomato"

        if self.Module_1 == None:
            # If there is no module then we mark it done
            button_color = "lime green"
            background = "lime green"
            self.Module_1_Done = True

        try:
            button = Button(self, bg=button_color, text=self.Module_1.name, font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_1"))
        except:
            button = Button(self, bg=button_color, text="None", font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_1"))
        button.grid(row=x, column=y, sticky=N+S+E+W,
                    padx=5, pady=5, columnspan=span)

    def Button2(self, x, y, span):
        # Here we set up the module
        try:
            # If the module is done we turn it green
            if self.Module_2.Module_Done == True:
                button_color = "lime green"
                background = "lime green"
            else:
                button_color = "tomato"
                background = "tomato"
        except:
            button_color = "tomato"
            background = "tomato"

        if self.Module_2 == None:
            # If there is no module then we mark it done
            button_color = "lime green"
            background = "lime green"
            self.Module_2_Done = True

        try:
            button = Button(self, bg=button_color, text=self.Module_2.name, font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_2"))
        except:
            button = Button(self, bg=button_color, text="Strike", font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.strike())
        button.grid(row=x, column=y, sticky=N+S+E+W,
                    padx=5, pady=5, columnspan=span)

    def Button3(self, x, y, span):
        # Here we set up the module
        try:
            # If the module is done we turn it green
            if self.Module_3.Module_Done == True:
                button_color = "lime green"
                background = "lime green"
            else:
                button_color = "tomato"
                background = "tomato"
        except:
            button_color = "tomato"
            background = "tomato"

        if self.Module_3 == None:
            # If there is no module then we mark it done
            button_color = "lime green"
            background = "lime green"
            self.Module_3_Done = True

        try:
            button = Button(self, bg=button_color, text=self.Module_3.name, font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_3"))
        except:
            button = Button(self, bg=button_color, text="None", font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_3"))
        button.grid(row=x, column=y, sticky=N+S+E+W,
                    padx=5, pady=5, columnspan=span)

    def Button4(self, x, y, span):
        # Here we set up the module
        try:
            # If the module is done we turn it green
            if self.Module_4.Module_Done == True:
                button_color = "lime green"
                background = "lime green"
            else:
                button_color = "tomato"
                background = "tomato"
        except:
            button_color = "tomato"
            background = "tomato"

        if self.Module_4 == None:
            # If there is no module then we mark it done
            button_color = "lime green"
            background = "lime green"
            self.Module_4_Done = True

        try:
            button = Button(self, bg=button_color, text=self.Module_4.name, font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_4"))
        except:
            button = Button(self, bg=button_color, text="None", font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_4"))
        button.grid(row=x, column=y, sticky=N+S+E+W,
                    padx=5, pady=5, columnspan=span)

    def Button5(self, x, y, span):
        # Here we set up the module
        try:
            # If the module is done we turn it green
            if self.Module_5.Module_Done == True:
                button_color = "lime green"
                background = "lime green"
            else:
                button_color = "tomato"
                background = "tomato"
        except:
            button_color = "tomato"
            background = "tomato"

        if self.Module_5 == None:
            # If there is no module then we mark it done
            button_color = "lime green"
            background = "lime green"
            self.Module_5_Done = True

        try:
            button = Button(self, bg=button_color, text=self.Module_5.name, font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_5"))
        except:
            button = Button(self, bg=button_color, text="None", font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_5"))
        button.grid(row=x, column=y, sticky=N+S+E+W,
                    padx=5, pady=5, columnspan=span)

    def Button6(self, x, y, span):
        # Here we set up the module
        try:
            # If the module is done we turn it green
            if self.Module_6.Module_Done == True:
                button_color = "lime green"
                background = "lime green"
            else:
                button_color = "tomato"
                background = "tomato"
        except:
            button_color = "tomato"
            background = "tomato"

        if self.Module_6 == None:
            # If there is no module then we mark it done
            button_color = "lime green"
            background = "lime green"
            self.Module_6_Done = True

        try:
            button = Button(self, bg=button_color, text=self.Module_6.name, font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_6"))
        except:
            button = Button(self, bg=button_color, text="None", font=("TexGyreAdventor", 25),
                            borderwidth=10, activebackground=background, command=lambda: self.Module_Setup("Module_6"))
        button.grid(row=x, column=y, sticky=N+S+E+W,
                    padx=5, pady=5, columnspan=span)

    
    def Module_Setup(self, Button):
        try:
            if Button == "Module_1":
                self.Module_1.main(self.Module_1_Started)
                if self.Module_1_Started == False:
                    self.Module_1_Started = True
                
                self.current_module = 1
        except:
            pass

        try:
            elif Button == "Module_2":
                self.Module_2.main(self.Module_2_Started)
                if self.Module_2_Started == False:
                    self.Module_2_Started = True
                
                self.current_module = 2
        except:
            pass

        try:
            elif Button == "Module_3":
                self.Module_3.main(self.Module_3_Started)
                if self.Module_3_Started == False:
                    self.Module_3_Started = True
                
                self.current_module = 3
        except:
            pass

        try:
            elif Button == "Module_4":
                self.Module_4.main(self.Module_4_Started)
                if self.Module_4_Started == False:
                    self.Module_4_Started = True
                
                self.current_module = 4
        except:
            pass

        try:
                
            elif Button == "Module_5":
                self.Module_5.main(self.Module_5_Started)
                if self.Module_5_Started == False:
                    self.Module_5_Started = True
                
                self.current_module = 5
        except:
            pass

        try:
            elif Button == "Module_6":
                self.Module_6.main(self.Module_6_Started)
                if self.Module_6_Started == False:
                    self.Module_6_Started = True
        
                self.current_module = 6
        except:
            pass


    def Game_Over(self):
        # Here we play the explosion sound and end music
        explode = pygame.mixer.Sound("music/death.wav")
        explode.play()
        pygame.mixer.music.load("music/defused.mp3")
        pygame.mixer.music.play(loops=-1)
        # Set up
        try:
            GPIO.cleanup()
        except:
            pass
        self.timer_pause = True
        self.Alive = False
        self.counter = None
        self.clearFrame()
        self.rows = 3
        self.cols = 3

        # GUI widget set up
        Time_Left = Label(self, text=f"Time Left:",
                         bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        Time_Left.grid(row=0, column=0, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=1, rowspan=1)

        Lose = Label(self, text=f"You Lose!",
                         bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        Lose.grid(row=0, column=1, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=1, rowspan=2)

        Strikes = Label(self, text=f"Strikes:",
                         bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        Strikes.grid(row=0, column=2, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=1, rowspan=1)
        
        self.countdown(1, 0, 1)
        self.health(1, 2, 1)

        start_over = Button(self, bg="red", text="Start Over", font=(
            "TexGyreAdventor", 25), borderwidth=10, activebackground="blue", command=lambda: self.reset())
        start_over.grid(row=2, column=0, sticky=N+S+E+W, padx=5, pady=5, columnspan=3)

        quit = Button(self, bg="dim gray", text="Quit", font=("TexGyreAdventor", 25),
                      borderwidth=10, activebackground="light grey", command=lambda: self.quit())
        quit.grid(row=3, column=0, sticky=N+S+E+W, padx=5, pady=5, columnspan=3)

        # Configure grid
        for row in range(self.rows):
            Grid.rowconfigure(self, row, weight=1)

        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 2, weight=1)


        self.pack(fill=BOTH, expand=True)

    def Game_Win(self):
        # Here we play end music
        pygame.mixer.music.load("music/defused.mp3")
        pygame.mixer.music.play(loops=-1)
        try:
            GPIO.cleanup()
        except:
            pass
        self.clearFrame()
        self.rows = 4
        self.cols = 3
        self.timer_pause = True

        # GUI widget set up
        Time_Left = Label(self, text=f"Time Left:",
                         bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        Time_Left.grid(row=0, column=0, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=1, rowspan=1)

        Win = Label(self, text=f"You Win!",
                         bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        Win.grid(row=0, column=1, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=1, rowspan=2)

        Strikes = Label(self, text=f"Strikes:",
                         bg="white", font=("TexGyreAdventor", 35), relief="groove", borderwidth=10)
        Strikes.grid(row=0, column=2, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=1, rowspan=1)

        self.countdown(1, 0, 1)
        self.health(1, 2, 1)

        start_over = Button(self, bg="red", text="Start Over", font=(
            "TexGyreAdventor", 25), borderwidth=10, activebackground="blue", command=lambda: self.reset())
        start_over.grid(row=2, column=0, sticky=N+S+E+W, padx=5, pady=5, columnspan=3, rowspan=1)

        quit = Button(self, bg="dim gray", text="Quit", font=("TexGyreAdventor", 25),
                      borderwidth=10, activebackground="light grey", command=lambda: self.quit())
        quit.grid(row=3, column=0, sticky=N+S+E+W, padx=5, pady=5, columnspan=3, rowspan=1)

        # Grid configure
        for row in range(self.rows):
            Grid.rowconfigure(self, row, weight=1)

        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 2, weight=1)

        self.pack(fill=BOTH, expand=True)



# create the window
window = Tk()
# set the window title
window.title("Continue Speaking And Everyone Lives")
window.geometry("800x400")
# generate the GUI
p = MainGUI(window)
# display the GUI and wait for user interaction
p.mainloop()
pygame.mixer.music.stop()
GPIO.cleanup()
