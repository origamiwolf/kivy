from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
from random import randint
from plyer import accelerometer
from functools import partial

## Leagoo accelerometer X,Y limits -9.5 to 9.5
## rest position of Y acceleration 3.0

class Arena(Widget):
    om = NumericProperty(0)
    colH = NumericProperty(0)
    colS = NumericProperty(0)
    colV = NumericProperty(0)
    col = ReferenceListProperty(colH, colS, colV)
    
    def updateOmUp(self):
        self.om += 1
        if (self.om > 10000):
            self.om = 10000
        self.col = (0.0001*self.om,1,1)

    def updateOmDown(self):
        self.om -= 100
        if (self.om < 0):
            self.om = 0
        self.col = (0.0001*self.om,1,1)

class Dot(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    oldPosX = NumericProperty(0)
    oldPosY = NumericProperty(0)
    oldPos = ReferenceListProperty(oldPosX,oldPosY)

    def move(self):
        self.oldPos = self.center
        self.pos = Vector(self.velocity) + Vector(self.pos)

        ## Check for boundaries
        if (self.x < 0):
            self.x = 0
            self.velocity_x = 0

        if (self.right > self.parent.width):
            self.right = self.parent.width
            self.velocity_x = 0            

        if (self.y < 0):
            self.y = 0
            self.velocity_y = 0

        if (self.top > self.parent.height):
            self.top = self.parent.height
            self.velocity_y = 0

    def drawTrail(self, *largs):
        with self.canvas:
            trailLine = Line(points=(self.center + self.oldPos))

            def removeTrail(trail, *largs):
                self.canvas.remove(trail)
            Clock.schedule_once(partial(removeTrail, trailLine), 1)
            
class Zen(Widget):
    dot = ObjectProperty(None)
    arena = ObjectProperty(None)
    accelX = NumericProperty(None)
    accelY = NumericProperty(None)

    def putDot(self):
        self.dot.center = self.center
        self.dot.velocity = Vector(0, 0)

    def putArena(self):
        self.arena.center = self.center
        self.arena.om = 0
    
    def update(self, dt):
        self.dot.move()
        self.dot.drawTrail()
        if (Vector(self.dot.center).distance(self.arena.center) > 100):
            self.arena.updateOmDown()
        else:
            self.arena.updateOmUp()
##        self.accelX = randint(-3,3)
##        self.accelY = randint(-3,3)
        val = accelerometer.acceleration[:3]
        self.accelX = -val[0]/100
        self.accelY = -(val[1]-3.0)/100
        self.dot.velocity_x += self.accelX
        self.dot.velocity_y += self.accelY
        
class ZenApp(App):
    def build(self):
        hg = Zen()
        hg.putArena()
        hg.putDot()
        accelerometer.enable()
        Clock.schedule_interval(hg.update, 1.0/60.0)
        return hg

if __name__ == '__main__':
    ZenApp().run()
