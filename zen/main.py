from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from random import randint
from plyer import accelerometer

## Leagoo accelerometer X,Y limits -9.5 to 9.5

class Dot(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
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
            
class Zen(Widget):
    dot = ObjectProperty(None)
    accelX = NumericProperty(None)
    accelY = NumericProperty(None)

    def putDot(self):
        self.dot.center = self.center
        self.dot.velocity = Vector(0, 0)
    
    def update(self, dt):
        self.dot.move()
##        self.accelX = randint(-3,3)
##        self.accelY = randint(-3,3)
        val = accelerometer.acceleration[:3]
        self.accelX = val[0]
        self.accelY = val[1]
##        self.dot.velocity_x += self.accelX
##        self.dot.velocity_y += self.accelY         
        
class ZenApp(App):
    def build(self):
        hg = Zen()
        hg.putDot()
        accelerometer.enable()
        Clock.schedule_interval(hg.update, 1.0/60.0)
        return hg

if __name__ == '__main__':
    ZenApp().run()
