import numpy as np   
import pyglet 
from points import x_points, y_points
 
     
 
def circle_points(center, radius, resolution = 36):

    angle_inc = 2 * np.pi / resolution

    angles = (angle_inc * i for i in range(resolution))

    points = tuple((center[0] + np.cos(angle) * radius, center[1] + np.sin(angle) * radius) for angle in angles)

    points = tuple(element for tupl in points for element in tupl)
    return points

 

WIDTH = 640
HEIGHT = 480
X_OFFSET = 0
Y_OFFSET = 0



class Main(pyglet.window.Window):
    def __init__ (self, width, height, x_points, y_points, x_circles, y_circles, orig):
        super().__init__(width, height)
        self.x_points = x_points
        self.y_points = y_points
        self.x_circles = x_circles
        self.y_circles = y_circles
        self.show_circles = True
        self.ends = []
        self.point_colors = []
        self.t = 0
        self.circle_colors = (150,50,150)
        self.lever_colors = (0, 150, 0)
        self.batch = pyglet.graphics.Batch()
        self.orig = orig
        
    def update(self, dt):
        self.t += dt

    def on_draw(self):

        self.clear()
        freq_scale = .1 #Scales how fast the circles spin and draw
        
        orig = self.orig
        
        for circle in self.y_circles:
            orig = self.spinning_circle(orig, circle[0], circle[2] * freq_scale, circle[1] + np.pi/2, False)
        
        for circle in self.x_circles:
            orig = self.spinning_circle(orig, circle[0], circle[2] * freq_scale, circle[1], True)
    
        self.ends.append(orig[0])
        self.ends.append(orig[1])
    
#        self.point_colors.append(int(np.cos(orig[0]/200 + orig[1]/200) * 255))
#        self.point_colors.append(int(np.sin(orig[0]/150 - orig[1]/150) * 255))
#        self.point_colors.append(len(self.ends) % 255)
        
        pyglet.graphics.draw(len(self.ends) // 2, pyglet.gl.GL_LINE_STRIP, 
                             ('v2f', self.ends),
                             ('c3B', (255,255,255) * (len(self.ends)//2)))
    
    def spinning_circle(self, orig, length, freq, starting_angle, width):
        if width:
            mid = (orig[0] + (length/2) * np.cos(np.pi * freq * self.t + starting_angle), orig[1] + (length/2) * np.sin(np.pi * freq * self.t + starting_angle))
            end = (mid[0] + mid[0] - orig[0], orig[1])
        else:
            mid = (orig[0] + (length/2) * np.cos(np.pi * freq * self.t + starting_angle), orig[1] + (length/2) * np.sin(np.pi * freq * self.t + starting_angle))
            end = (orig[0], mid[1] + mid[1] - orig[1])
        
        resolution = 32
        angle_inc = np.pi * 2 / resolution
        
        if self.show_circles:
            
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (orig[0], orig[1], mid[0], mid[1])),
                             ('c3B', self.lever_colors * 2))
    
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (mid[0], mid[1], end[0], end[1])),
                             ('c3B', self.lever_colors * 2))
            
            circle_points1 = [(orig[0] + (length / 2) * np.cos(angle_inc * i), orig[1] + (length / 2) * np.sin(angle_inc * i)) for i in range(resolution)]
            circle_points1 = tuple(element for tupl in circle_points1 for element in tupl)
            circle_points1 = circle_points1 + (circle_points1[0], circle_points1[1])
            pyglet.graphics.draw(resolution + 1, pyglet.gl.GL_LINE_STRIP,  
                             ('v2f', circle_points1), ('c3B', self.circle_colors*(resolution + 1)))
            
            circle_points2 = [(mid[0] + (length / 2) * np.cos(angle_inc * i), mid[1] + (length / 2) * np.sin(angle_inc * i)) for i in range(resolution)]
            circle_points2 = tuple(element for tupl in circle_points2 for element in tupl)
            circle_points2 = circle_points2 + (circle_points2[0], circle_points2[1])
            pyglet.graphics.draw(resolution + 1, pyglet.gl.GL_LINE_STRIP,  
                             ('v2f', circle_points2), ('c3B', self.circle_colors*(resolution+1)))
    
        return end
    
        
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.S:
            self.show_circles = not self.show_circles

def fourier_circles_points(points, T, N, tolerance=1):
    f_sample = 2 * N
    t, dt = np.linspace(0, T, f_sample + 2, endpoint=False, retstep=True)
    y = np.fft.rfft(points) / t.size
    y *= 2
    
    offset = y[0].real
    radii = abs(y[1:-1])
    freqs = np.arange(1, len(y) - 1) #TODO: Fix this to handle actual scale of frequencies
    angles = np.arctan2(y[1:-1].imag, y[1:-1].real)
    
    select = np.where(radii > tolerance)
    
    return offset, radii[select], angles[select], freqs[select]


T = 1
x_circles = []
N = len(x_points)//2 - 2
x_offset, x_radii, x_angles, x_freqs = fourier_circles_points(x_points, T, N)
for xr, xa, xf in zip(x_radii, x_angles, x_freqs):
    x_circles.append([xr, xa, xf])

y_circles = []
y_offset, y_radii, y_angles, y_freqs = fourier_circles_points(y_points, T, N)
for yr, ya, yf in zip(y_radii, y_angles, y_freqs):
    y_circles.append([yr, ya, yf])

orig = (int(np.min(x_points) + np.max(x_points))//2, int(np.min(y_points) + np.max(y_points))//2)

if __name__ == '__main__':
    game_window = Main(WIDTH, HEIGHT, x_points, y_points, x_circles, y_circles, orig)
    pyglet.clock.schedule_interval(game_window.update, 1/60)

    pyglet.app.run()
