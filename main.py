from manim import *
import numpy as np

class GerstnerWave(Scene):
    def construct(self):
        nx = 32
        ny = 8
        dotspace = 1/2

        tracker = ValueTracker(0)
        self.add(tracker)
        dots = VGroup()

        wavelen = 8
        height = 1

        for ix in range(nx):
            for iy in range(ny):
                px = (ix - nx / 2) * dotspace
                py = (iy - ny) * dotspace

                dot = Dot(radius=0.1)
                offs = wavegetoffset(px, py, 0, wavelen, height)
                dot.move_to([offs[0] + px, offs[1] + py, 0])
                depth = -py / (ny * dotspace)
                color = interpolate_color(RED, BLUE, depth)
                dot.set_color(color)

                # Gerstner-style wave offset in y
                def updater(d, px=px, py=py, wavelen=wavelen, height=height):
                    t = tracker.get_value()
                    offs = wavegetoffset(px, py, t, wavelen, height)
                    d.move_to([offs[0] + px, offs[1] + py, 0])

                dot.add_updater(updater)
                dots.add(dot)

        self.add(dots)

        k = 2 * np.pi / wavelen
        g = 9.8
        c = np.sqrt(g / k)
        T = 2 * np.pi / (k * c)

        def update_tracker(mob, dt):
            current = mob.get_value()
            if current < T:
                mob.set_value(min(current + dt, T))

        tracker.add_updater(update_tracker)

        self.wait(T)
        tracker.remove_updater(update_tracker)

        #self.play(tracker.animate.set_value(T), run_time=T, rate_func=linear)

        ix = nx / 2
        iy = ny / 2
        px = (ix - nx / 2) * dotspace
        py = (iy - ny) * dotspace

def wavegetoffset(a, b, t, wavelength, A=1):
    k = 2 * np.pi / wavelength
    g = 9.8
    c = np.sqrt(g / k)
    x =  A * np.exp(-k * abs(b)) * np.sin(k * (a + c * t))
    y = -A * np.exp(-k * abs(b)) * np.cos(k * (a + c * t))
    return [x, y]