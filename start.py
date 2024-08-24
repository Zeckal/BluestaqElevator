

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
    elevators = []
    callButtons = []
    def __init__ (self,floors,elevators):
        for x in range (1,elevators+1):
            self.AddElevator(floors+1,x)
        for y in range (1,floors+1):
            self.AddCallButton(y)
        
    def AddElevator(self,floors,name):
        self.elevators.append(Elevator(floors,name))
        
    def AddCallButton(self,floor):
        self.callButtons.append(CallButton(floor))
        
    def Cycle(self):
        for e in self.elevators:
            e.Cycle(self.callButtons,self.elevators)
            
    def Print(self):
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
        #cycle function does one action per time it is called, this could be changed to a countdown if timespands needed to be non-uniform
        
        
        otherTargets = []
        for elv in otherElevators:
            otherTargets.append(elv.targetFloor)
            
        
        if self.doorsOpen == 1:
            #if the doors are open, close the doors
            self.doorsOpen = 0
            
        elif self.movement == 1:
            if callButtons[self.currentFloor-1].upButtonPressed == 1 or self.pannelButtons[self.currentFloor-1].pressed == 1:
                #if the doors are closed, check if they need to be opened, it is traveling upwards, so do not open for callbutton downards
                self.doorsOpen = 1
                #garunteed doors are closed due to first if block in cycle function
                
                callButtons[self.currentFloor-1].upButtonPressed = 0
                self.pannelButtons[self.currentFloor-1].pressed = 0
                
                #turn the call and pannel buttons off as it has opened for this floor now
               
            if self.doorsOpen == 0 and self.currentFloor != self.floorMax:
                #it didn't need to open doors, check if it needs to continue upwards
                for uup in range (self.currentFloor,self.floorMax):
                    #only check floors above current floor
                    if uup not in otherTargets and (self.pannelButtons[uup-1].pressed == 1 or callButtons[uup-1].upButtonPressed == 1 or callButtons[uup-1].downButtonPressed == 1):
                        #if any floor above has been pressed, keep traveling upwards
                        self.targetFloor = uup
            
            if self.doorsOpen == 0 and self.currentFloor == self.targetFloor:
                #if it doesn't need to continue upwards, check if it needs to go downwards
                for udwn in range (self.floorMin-1,self.currentFloor):
                    #only check floors above current floor
                    if(self.pannelButtons[udwn-1].pressed == 1 or callButtons[udwn-1].upButtonPressed == 1 or callButtons[udwn-1].downButtonPressed == 1):
                        #if any floor below has been pressed, change to traveling downwards
                        self.targetFloor = udwn
                        self.movement = -1
            if self.doorsOpen == 0 and self.currentFloor == self.targetFloor:
                #if no new target floor was found, stop
                self.movement = 0
            if self.movement == 1 and self.doorsOpen == 0:
                self.currentFloor += 1
            
        elif self.movement == -1:
            if callButtons[self.currentFloor-1].downButtonPressed == 1 or self.pannelButtons[self.currentFloor-1].pressed == 1:
                #if the doors are closed, check if they need to be opened, it is traveling downwards, so do not open for callbutton upwards
                
                self.doorsOpen = 1
                #garunteed doors are closed due to first if block in cycle function
                
                callButtons[self.currentFloor-1].downButtonPressed = 0
                self.pannelButtons[self.currentFloor-1].pressed = 0
                #turn the call and pannel buttons off as it has opened for this floor now
                
            if self.doorsOpen == 0 and self.currentFloor != self.floorMin:
                #it didn't need to open doors, check if it needs to continue downwards
                for ddwn in range (self.floorMin-1,self.currentFloor):
                    #only check floors below current floor
                    if ddwn not in otherTargets and (self.pannelButtons[ddwn-1].pressed == 1 or callButtons[ddwn-1].upButtonPressed == 1 or callButtons[ddwn-1].downButtonPressed == 1):
                        #if any floor below has been pressed, keep traveling downwards
                        self.targetFloor = ddwn 
            if self.currentFloor == self.targetFloor:
                #if it doesn't need to continue upwards, check if it needs to go downwards
                for dup in range (self.currentFloor+1,self.floorMax):
                    #only check floors above current floor
                    if(self.pannelButtons[dup-1].pressed == 1 or callButtons[dup-1].upButtonPressed == 1 or callButtons[dup-1].downButtonPressed == 1):
                        #if any floor below has been pressed, change to traveling downwards
                        self.targetFloor = dup
                        self.movement = 1
            if self.currentFloor == self.targetFloor:
                #if no new target floor was found, stop
                self.movement = 0
            if self.movement == -1 and self.doorsOpen == 0:
                self.currentFloor += -1
                
        elif self.movement == 0:
            if self.pannelButtons[self.currentFloor-1].pressed == 1 or callButtons[self.currentFloor-1].downButtonPressed == 1 or callButtons[self.currentFloor-1].upButtonPressed == 1:
                self.doorsOpen == 1
                #garunteed doors are closed due to first if block in cycle function
                
                
                
                callButtons[self.currentFloor-1].downButtonPressed = 0
                callButtons[self.currentFloor-1].upButtonPressed = 0
                self.pannelButtons[self.currentFloor-1].pressed = 0
                #turn the call and pannel buttons off as it has opened for this floor now
                
            distance = 0
            for floor in range(self.floorMin,self.floorMax):
                # find the closest floor that has been called
                if(self.pannelButtons[floor-1].pressed == 1 or (floor not in otherTargets and (callButtons[floor-1].upButtonPressed == 1 or callButtons[floor-1].downButtonPressed == 1))):
                    if distance == 0 or distance > abs(self.currentFloor - floor):
                        distance = abs(self.currentFloor - floor)
                        self.targetFloor = floor
                
                        
            if self.targetFloor > self.currentFloor:
                self.movement = 1
            elif self.targetFloor < self.currentFloor:
                self.movement = -1
            else:
                self.movement = 0
         
if __name__ == '__main__':
    main()