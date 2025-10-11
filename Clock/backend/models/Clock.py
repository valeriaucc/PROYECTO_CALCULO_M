from .NodeHours import NodeHours
from .Hours import Hours

class Clock:
    def __init__(self):
        self.firstHour = None
    
    def insertHourStart(self, Hours):
        first = NodeHours(Hours)
        if self.firstHour is None:
            self.firstHour = first
            first.nextHours = self.firstHour
            first.prevHours = self.firstHour
        else:
            second = self.firstHour.prevHours
            first.nextHours = self.firstHour
            self.firstHour.prevHours = first
            first.prevHours = second
            second.nextHours = first
            self.firstHour = first

    def insertHoursEnd(self, Hours):
        second = NodeHours(Hours)
        if self.firstHour is None:
            self.firstHour = second
            second.nextHours = self.firstHour
            second.prevHours = self.firstHour
        else:
            last = self.firstHour.prevHours
            last.nextHours = second
            second.nextHours = self.firstHour
            second.prevHours = last
            self.firstHour.prevHours = second
    
    def deleteHour(self, Hours):
        if self.firstHour is None:
            print("No hay horas que eliminar")
            return
        
        currentHour = self.firstHour

       
        if currentHour.Hours == Hours:
            if currentHour.nextHours == self.firstHour:
                self.firstHour = None
            else:
                last = self.firstHour.prevHours
                self.firstHour = currentHour.nextHours
                self.firstHour.prevHours = last
                last.nextHours = self.firstHour
            return
        
        while currentHour.nextHours != self.firstHour:
            if currentHour.Hours == Hours:
                currentHour.prevHours.nextHours = currentHour.nextHours
                currentHour.nextHours.prevHours = currentHour.prevHours
                return
            currentHour = currentHour.nextHours

        if currentHour.Hours == Hours:
            currentHour.prevHours.nextHours = self.firstHour
            self.firstHour.prevHours = currentHour.prevHours

    def printHours(self):
        if self.firstHour is None:
            print("No hay horas registradas")
            return
        
        currentHour = self.firstHour
        print(currentHour.Hours)
        currentHour = currentHour.nextHours
        
        while currentHour != self.firstHour:
            print(currentHour.Hours)
            currentHour = currentHour.nextHours