# Here is where we import all the modules for the program
from tkinter import *
# import RPi.GPIO as GPIO
from random import *
from math import *
from time import *
import pygame


# This is the main GUI

class MainGUI(Frame):
    def __init__(self, parent):
        # Here we inherit all the tkinter Frame functions to be used in the rest of the program
        Frame.__init__(self, parent, bg="light grey")
        # Here we setg the program to open in full screen and to show no cursor on the raspberry pi
        parent.attributes("-fullscreen", False)
        # self.config(cursor="none")
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
        # GPIO.output(pin, signal);
        pass
        return
    
    # In order to save space in the init and also to allow for easy and clean reseting when the user starts over, we store all the class variable
    # and other set up resourses in the reset function
    def reset(self):
        # try:
        #     pass
        #     GPIO.cleanup()
        # except:
        #     pass
        self.loc = "Home"
        self.current_module = None
        self.counter = None
        
        # Here we run the program for the start screen
        self.MainMenu()

    def MainMenu(self):
        # Here we run the function to play the main music for the game
        # self.play_main_music()
        # try:
        #     pass
        #     GPIO.cleanup()
        # except:
        #     pass
    
        # Set up
        self.clearFrame()
        self.loc="Home"
        self.cols = 1
        self.rows = 4

        # Here we set the current module (0 for Home) so that it the program is paused, it will resume.
        self.current_module = 0

        # Here we call a function for various predefined buttons
        # The first 4 will be called in almost every screen/module
        # The last 6 will be called for the main menu every time
        self.location(0, 0, 1)
        self.mode(0, 1, 1)
 

        for row in range(self.rows):
            Grid.rowconfigure(self, row, weight=1)
        for col in range(self.cols):
            Grid.columnconfigure(self, col, weight=1)

        self.pack(fill=BOTH, expand=True)


    def clearFrame(self):
        # Clean up gpio
        # try:
        #     pass
        #     GPIO.cleanup()
        # except:
        #     pass
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
            

    def location(self, x, y, span):
        # Here we set up the location widget
        location = Label(self, text=f"{self.loc}", bg="white", font=("TexGyreAdventor", 15), relief="groove", borderwidth=3)
        location.grid(row=y, column=x, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=span)

    def time(self, x, y, span):
        # Here we set up the location widget
        time = Label(self, text=f"{self.time}", bg="white", font=("TexGyreAdventor", 15), relief="groove", borderwidth=3)
        time.grid(row=y, column=x, sticky=N+S+E+W,
                      padx=5, pady=5, columnspan=span)

    def mode(self, x, y, span):
        mode = Button(self, bg="gray", text="Mode", font=("TexGyreAdventor", 15), relief="groove", borderwidth=3, activebackground="light grey", command=lambda: self.Module_Setup("Module_1"))
        mode.grid(row=y, column=x, sticky=N+S+E+W,
                    padx=5, pady=5, columnspan=span)

    def back_button(self, x, y, span):
        # Here we set up the back button widget
        back_button = Button(self, bg="gray", text="Back", font=("TexGyreAdventor", 15), relief="groove", borderwidth=3, activebackground="light grey", command=lambda: self.MainMenu())
        back_button.grid(row=y, column=x, sticky=N+S+E+W, pady=5, columnspan=span)

# create the window
window = Tk()
# set the window title
window.title("Lightswitch Advaned")
window.geometry("320x480")
# generate the GUI
p = MainGUI(window)
# display the GUI and wait for user interaction
p.mainloop()
pygame.mixer.music.stop()
# GPIO.cleanup()
