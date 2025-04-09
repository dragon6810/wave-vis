from manim import *
import numpy as np

class GerstnerWave(Scene):
    def construct(self):
        nx = 32
        ny = 8
        dotspace = 1/2

        tracker = ValueTracker(0)
        dots = VGroup()

        wavelen = 16
        height = 1

        for ix in range(nx):
            for iy in range(ny):
                px = (ix - nx / 2) * dotspace
                py = (iy - ny) * dotspace

                dot = Dot(radius=0.1)
                dot.move_to([wavegetx(px, py, 0, wavelen), wavegety(px, py, 0, wavelen), 0])
                depth = -py / (ny * dotspace)
                color = interpolate_color(RED, BLUE, depth)
                dot.set_color(color)

                # Gerstner-style wave offset in y
                def updater(d, px=px, py=py, wavelen=wavelen, height=height):
                    t = tracker.get_value()
                    d.move_to([wavegetx(px, py, t, wavelen, height), wavegety(px, py, t, wavelen, height), 0])

                dot.add_updater(updater)
                dots.add(dot)

        self.add(dots)

        k = 2 * np.pi / wavelen
        g = 9.8
        c = np.sqrt(g / k)
        T = 2 * np.pi / (k * c)
        self.play(tracker.animate.set_value(T), run_time=T, rate_func=linear)
    
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