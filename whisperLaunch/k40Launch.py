### k40 Whisperer is a program Reed uses to run a laser cutter.

### This file is dedicated to solving the issue of "I no longer own a Laptop."
#       The laser cutter needs a laptop to open k40 and run a file saved on it.
#       I propose we use an aduino or raspberry pie to open a file from a flashdrive
#           and run it from there.

# Software Design Specs:
    # The software needs to run a file in k40 whisperer
    # The software needs to allow jog and all other things Reed normally uses from the laptop
        # There is a picture of the interface included in this file.
    # !!! Originally i assumed it would be as simple as launching the program but I am now
        # realising that all GUI functionality will be required.



class k40item:
    # Let's define some of the functionality an instance would be required to have.
    def __init__(self,):
        print("I'm alive.")
    def heartbeat(self,):
        # Check if instance is initialized.
        print('boink')
    def initializeCut(self,):
        # Initialize the cutting of laser.
        pass
    def openFile(self,):
        # open a file
        pass
    def reloadFile(self,):
        pass
    def home(self,):
        pass
    def unlockRail(self,):
        pass
    def setJog(self,):
        pass
    def moveTo(self,X,Y):
        pass
    def setRaster(self,speed):
        pass
    def setVector(self,speed):
        pass
    def setCut(self,speed):
        pass
    def pause(self,):
        pass
    def stop(self,):
        pass

