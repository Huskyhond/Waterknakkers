#--------------------------------
#Boris van Norren
#Hogeschool Rotterdam
#0835560
#TI3A
#Waterknakkers
#--------------------------------

class Coords(self, coordinates):
    def __init__(self):
        # Get the boat's coordinates
        self.coordinates = 0
        # Calculate the angle from the boat towards the given coordinates the boat is supposed to go
        self.angle = coordinates - self.coordinates

    #change incoming value in set range to value in other given range
    def map(self, x, in_min, in_max, out_min, out_max):
        return np.clip(int(((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)*100 )/100,out_min,out_max)

    def calcBoatAngle(self):
        northcoords = 0

    def calcBoatAngleDifference(self):
        # Adjust the boat angularly
        if(calcBoatAngle != self.angle):
            turnBoat(calcBoatAngle - self.angle)

    def turnBoat(self, angle):
        if(angle > 0):
            # Turn clockwise
            return 0
        elif(angle < 0):
            # Turn counter clockwise
            return 0