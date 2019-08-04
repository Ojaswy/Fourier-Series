# -*- coding: utf-8 -*-
import numpy as np
import pickle
import pyglet 
from pyglet.window import mouse



 
class Main(pyglet.window.Window): 
    def __init__ (self):
        super().__init__(640, 480)
        self.x_points = []
        self.y_points = []
        self.batch = pyglet.graphics.Batch()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.x_points.append(x)
        self.y_points.append(y)
        
    def update(self, dt):
        for x, y in zip(self.x_points, self.y_points):
            self.batch.add(1, pyglet.gl.GL_POINTS, None,
                         ('v2f', (x, y)))

    def on_draw(self):
        global batch
        self.clear()
        self.batch.draw()


 
if __name__ == '__main__': 
    window = Main()
    pyglet.clock.schedule_interval(window.update, 1/60)

    pyglet.app.run()
    
    
    window.x_points = window.x_points
    window.y_points = window.y_points
    pickle.dump((window.x_points, window.y_points), open("xy_points.p", "wb"))
    
x_points, y_points = pickle.load(open("xy_points.p", "rb"))

