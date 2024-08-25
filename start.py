# By Andrew Shaw 8/24/2024

def main():
   
   elvNumb = int(input("Enter number of elevators: "))   
   florNumb = int(input("Enter number of floors: "))
   cycleInput = input("Enter elevator command: ")
   theBuilding = Building(florNumb, elvNumb)
   while cycleInput != "esc":
       if cycleInput == "help":
           print("you can press call buttons or elevator pannel buttons each cycle")
           print("If you want to enter multiple commands in 1 cycle separate each with a '|'")
           print("To press the elevator call button on a floor enter in the format c.[FLOOR].[up/down] Ex: c.2.up")
           print("To press an elevator pannel button for a floorm enter in the format e.[ElevatorNumber].[FLOOR] Ex: e.2.2")
       elif cycleInput != "esc":
           cmds = cycleInput.split("|")
           for cmd in cmds:
               parts = cmd.split(".")
               if parts[0] == "c":
                   if(parts[2] == "up"):
                       theBuilding.callButtons[int(parts[1])-1].upButtonPressed = 1
                   elif(parts[2] == "down"):
                       theBuilding.callButtons[int(parts[1])-1].downButtonPressed = 1
               elif parts[0] == "e":
                   theBuilding.elevators[int(parts[1])-1].pannelButtons[int(parts[2])-1].pressed = 1
       theBuilding.Cycle()
       theBuilding.Print()
       print("Enter command, or Enter 'help' for details or 'esc' to exit")
       cycleInput = input() 

class Building(object):
    #object to hold the data model that it interacted with
    elevators = []
    callButtons = []
    def __init__ (self,floors,elevators):
        for x in range (1,elevators+1):
            self.AddElevator(floors+1,x)
        for y in range (1,floors+1):
            self.AddCallButton(y)
        
    def AddElevator(self,floors,name):
        #constructor assitant function
        self.elevators.append(Elevator(floors,name))
        
    def AddCallButton(self,floor):
        #constructor assitant function
        self.callButtons.append(CallButton(floor))
        
    def Cycle(self):
        #step to the next moment in time, make all the elevators take their next action
        for e in self.elevators:
            e.Cycle(self.callButtons,self.elevators)
            
    def Print(self):
        #print out all internal objects for console display
        for elv in self.elevators:
            elv.print()
        for callbutton in self.callButtons:
            callbutton.print()
        

class CallButton(object):
    #each floor's up and down call buttons
    def __init__ (self,floor):
        self.floorNumber = floor
        self.upButtonPressed = 0
        self.downButtonPressed = 0
    
    def print(self):
        print(self.floorNumber, ":", self.upButtonPressed, ":", self.downButtonPressed)

class PanelButton(object):
    # a single floor button in a elevator
    def __init__(self,floor):
        self.floorNumber = floor
        self.pressed = 0
        
class Elevator(object):
    #name = ""
    # represents the button panel in an elevator
    #pannelButtons = []
    # elevators current position
    #currentFloor = 0
    # where an elevator will stop next
    #targetFloor = 0
    #max floor
    #floorMax = 0
    #min floor
    #floorMin = 0
    # directon an elevator is moving
    #movement = 0
    # door open or closed
    #doorsOpen = 0
    
    def __init__(self,numberOfFloors, name):
        # start an elevator at ground floor, unmoving, with specified number of floors
        self.name = name
        self.currentFloor = 1
        self.targetFloor = 1
        self.floorMin = 1
        self.floorMax = numberOfFloors
        self.doorsOpen = 0
        self.pannelButtons = []
        self.movement = 0
        for x in range (1,numberOfFloors+1):
            self.AddButton(x)
        
    def AddButton(self,floorNumber):
        # Constructor helper to adding buttons to the elevator button panel
        self.pannelButtons.append(PanelButton(floorNumber))

    def ButtonPress(self,floorNumber):
        # activate button pressed value on a panel button
        self.pannelButtons[floorNumber-1].pressed = 1
        
    def PrintButtons(self):
        #prints out the button like in it's current state
        for x in self.pannelButtons:
            print(x.floorNumber, ":", x.pressed, end =" || ")
            
    def print(self):
        print()
        print("||||||||",self.name,"||||||||")
        print("Current Floor: ",self.currentFloor)
        print("Target Floor: ",self.targetFloor)
        print("Doors Open: ",self.doorsOpen)
        print("Movement Direction: ", self.movement)
        self.PrintButtons()
        print()

    def Move(self,direction):
        if direction == 0 or direction == 1 or direction == -1:
            self.movement = direction
            self.currentFloor += direction
            
    def Cycle(self, callButtons, otherElevators):
        #make the elevator take it's next action
        #elevators need to check 4 main things to determine what it is doing
        # 1: what direction it is currently traveling
        # 2: if any of it's buttons have been pressed
        # 3: if any call buttons have been pressed
        # 4: if any other elevator is already traveling to a location
        # 5: less important - is if it needs to close it's own doors
        
        #make a list of all currently targeted floors
        otherTargets = []
        for elv in otherElevators:
            otherTargets.append(elv.targetFloor)
            
        #close doors if they are open, this will be the action the elevator takes this cycle
        if self.doorsOpen == 1:
            self.doorsOpen = 0
        
        #if it is moving upwards
        elif self.movement == 1:
                #check if the upwards call button or it's own panel button has been pressed for this floor
                #if so, open the doors and turn off the buttons
            if callButtons[self.currentFloor-1].upButtonPressed == 1 or self.pannelButtons[self.currentFloor-1].pressed == 1:
                self.doorsOpen = 1
                callButtons[self.currentFloor-1].upButtonPressed = 0
                self.pannelButtons[self.currentFloor-1].pressed = 0
            
            #check if it didn't just open it's doors and if it needs to continue upwards to another floor
            if self.doorsOpen == 0 and self.currentFloor != self.floorMax:
                for uup in range (self.currentFloor,self.floorMax):
                    #only check floors above current floor
                    if uup not in otherTargets and (self.pannelButtons[uup-1].pressed == 1 or callButtons[uup-1].upButtonPressed == 1 or callButtons[uup-1].downButtonPressed == 1):
                        #if any floor above has been pressed, keep traveling upwards
                        self.targetFloor = uup
            #check if it's doors didn't just open and if it needs to descend to another floor
            if self.doorsOpen == 0 and self.currentFloor == self.targetFloor:
                for udwn in range (self.floorMin-1,self.currentFloor):
                    #only check floors above current floor
                    if(self.pannelButtons[udwn-1].pressed == 1 or callButtons[udwn-1].upButtonPressed == 1 or callButtons[udwn-1].downButtonPressed == 1):
                        #if any floor below has been pressed, change to traveling downwards
                        self.targetFloor = udwn
                        self.movement = -1
            #if no new destination is found, stop moving
            if self.doorsOpen == 0 and self.currentFloor == self.targetFloor:
                self.movement = 0
            #if it didn't need to stop at this floor, continue upwards
            if self.movement == 1 and self.doorsOpen == 0:
                self.currentFloor += 1
         
        #if it is moving downwards   
        elif self.movement == -1:
            #check if the downwards call button or it's own panel button has been pressed for this floor
            #if so, open the doors and turn off the buttons
            if callButtons[self.currentFloor-1].downButtonPressed == 1 or self.pannelButtons[self.currentFloor-1].pressed == 1:
                self.doorsOpen = 1
                callButtons[self.currentFloor-1].downButtonPressed = 0
                self.pannelButtons[self.currentFloor-1].pressed = 0
                
            #check if it didn't just open it's doors and if it needs to continue downwards to another floor
            if self.doorsOpen == 0 and self.currentFloor != self.floorMin:
                for ddwn in range (self.floorMin-1,self.currentFloor):
                    #only check floors below current floor
                    if ddwn not in otherTargets and (self.pannelButtons[ddwn-1].pressed == 1 or callButtons[ddwn-1].upButtonPressed == 1 or callButtons[ddwn-1].downButtonPressed == 1):
                        #if any floor below has been pressed, keep traveling downwards
                        self.targetFloor = ddwn 
            #check if it's doors didn't just open and if it needs to ascend to another floor
            if self.currentFloor == self.targetFloor:
                for dup in range (self.currentFloor+1,self.floorMax):
                    #only check floors above current floor
                    if(self.pannelButtons[dup-1].pressed == 1 or callButtons[dup-1].upButtonPressed == 1 or callButtons[dup-1].downButtonPressed == 1):
                        #if any floor above has been pressed, change to traveling upwards
                        self.targetFloor = dup
                        self.movement = 1
                        
            #if no new destination is found, stop moving
            if self.currentFloor == self.targetFloor:
                self.movement = 0
            #if it didn't need to stop at this floor, continue downwards
            if self.movement == -1 and self.doorsOpen == 0:
                self.currentFloor += -1
        
        #if it is not moving
        elif self.movement == 0:
            #check to see if the buttons on it's current floor have been pressed
            #if so, open the doors and turn off the buttons
            #this time both upwards and downwards buttons get reset since the elevator didn't have any initial direction
            if self.pannelButtons[self.currentFloor-1].pressed == 1 or callButtons[self.currentFloor-1].downButtonPressed == 1 or callButtons[self.currentFloor-1].upButtonPressed == 1:
                self.doorsOpen == 1
                callButtons[self.currentFloor-1].downButtonPressed = 0
                callButtons[self.currentFloor-1].upButtonPressed = 0
                self.pannelButtons[self.currentFloor-1].pressed = 0
                
            #next check if any buttons have been pressed that are not already targeted by another elevator
            distance = 0
            for floor in range(self.floorMin,self.floorMax):
                # find the closest floor that has been called
                if(self.pannelButtons[floor-1].pressed == 1 or (floor not in otherTargets and (callButtons[floor-1].upButtonPressed == 1 or callButtons[floor-1].downButtonPressed == 1))):
                    if distance == 0 or distance > abs(self.currentFloor - floor):
                        distance = abs(self.currentFloor - floor)
                        self.targetFloor = floor
                
            #if the target is above, start moving upwards            
            if self.targetFloor > self.currentFloor:
                self.movement = 1
            #if the target is below, start moving downwards   
            elif self.targetFloor < self.currentFloor:
                self.movement = -1
            else:
                self.movement = 0
         
if __name__ == '__main__':
    main()