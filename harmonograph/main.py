from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from random import randint
import math

class Dot(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    accel_x = NumericProperty(0)
    accel_y = NumericProperty(0)
    accel = ReferenceListProperty(accel_x, accel_y)
    omega = NumericProperty(0)
    radius = NumericProperty(0)
    delta = NumericProperty(0)

    def move(self):
        newpos = Vector(self.velocity) * self.delta + Vector(self.pos)
        self.accel = Vector(-((self.x - self.parent.center_x) * self.omega ** 2), \
                            -((self.y - self.parent.center_y) * self.omega ** 2))
        self.velocity = Vector(self.accel) * self.delta + Vector(self.velocity)
        self.pos = newpos

class MyHarmonograph(Widget):
    dot = ObjectProperty(None)

    def putDot(self):
        self.dot.center = self.center
        self.dot.radius = 50.0
        self.dot.x = self.center_x + self.dot.radius
        self.dot.y = self.center_y
        self.dot.omega = 2.0*math.pi
        self.dot.velocity = Vector(0, self.dot.omega*self.dot.radius)
        self.dot.delta = 1/60.0
    
    def update(self, dt):
        self.dot.move()
        
class MyHarmonographApp(App):
    def build(self):
        hg = MyHarmonograph()
        hg.putDot()
        Clock.schedule_interval(hg.update, 1.0/60.0)
        return hg

if __name__ == '__main__':
    MyHarmonographApp().run()
