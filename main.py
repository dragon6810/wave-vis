from manim import *
import numpy as np

class GerstnerWave(Scene):
    def construct(self):
        nx = 32
        ny = 16
        dotspace = 1/2

        tracker = ValueTracker(0)
        dots = VGroup()

        for ix in range(nx):
            for iy in range(ny):
                px = (ix - nx / 2) * dotspace
                py = (iy - ny) * dotspace
                dot = Dot(radius=0.04)
                wavelen = 16
                height = 1
                dot.move_to([wavegetx(px, py, 0, wavelen), wavegety(px, py, 0, wavelen), 0])

                # Gerstner-style wave offset in y
                def updater(d, px=px, py=py, wavelen=wavelen, height=height):
                    t = tracker.get_value()
                    d.move_to([wavegetx(px, py, t, wavelen, height), wavegety(px, py, t, wavelen, height), 0])

                dot.add_updater(updater)
                dots.add(dot)

        self.add(dots)
        self.play(tracker.animate.set_value(4), run_time=4, rate_func=linear)
        #self.wait(4)
    
def wavegetx(a, b, t, wavelength, A=0.1):
    k = 2 * np.pi / wavelength
    g = 9.8
    c = np.sqrt(g / k)
    return a + A * np.exp(-k * abs(b)) * np.sin(k * (a + c * t))

def wavegety(a, b, t, wavelength, A=0.1):
    k = 2 * np.pi / wavelength
    g = 9.8
    c = np.sqrt(g / k)
    return b - A * np.exp(-k * abs(b)) * np.cos(k * (a + c * t))