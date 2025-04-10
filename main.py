from manim import *
import numpy as np

class GerstnerWave(Scene):
    def construct(self):
        nx = 32
        ny = 8
        dotspace = 1/2
        circlespace = 4
        circley = ny - 1

        tracker = ValueTracker(0)
        self.add(tracker)
        circledots = VGroup()
        alonedots = VGroup()

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

                if(ix % circlespace != 0 or iy != circley):
                    alonedots.add(dot)
                else:
                    circledots.add(dot)

        self.add(circledots)
        self.add(alonedots)

        k = 2 * np.pi / wavelen
        g = 9.8
        c = np.sqrt(g / k)
        T = 2 * np.pi / (k * c)

        def update_tracker(mob, dt):
            current = mob.get_value()
            mob.set_value(current + dt)

        tracker.add_updater(update_tracker)

        self.wait(T)

        circles = VGroup()

        for ix in range(0, nx, circlespace):
            iy = circley
            px = (ix - nx / 2) * dotspace
            py = (iy - ny) * dotspace
            offs = wavegetoffset(px, py, 0, wavelen, height)
            
            circle = Circle(radius=np.sqrt(offs[0]**2+offs[1]**2))
            circle.move_to([px, py, 0])
            circle.set_fill(PINK, opacity=0.2)
            circles.add(circle)

        self.play(Create(circles, run_time=1.0), *[dot.animate.set_opacity(0.2) for dot in alonedots])

        self.wait(T*2-1.0)

        self.play(Uncreate(circles, run_time=1.0), *[dot.animate.set_opacity(1.0) for dot in alonedots])

        self.wait(T-1.0)

        tracker.remove_updater(update_tracker)

def wavegetoffset(a, b, t, wavelength, A=1):
    k = 2 * np.pi / wavelength
    g = 9.8
    c = np.sqrt(g / k)
    radius = A * np.exp(k * b)
    theta = k * (a + c * t)

    x =  radius * np.sin(theta)
    y = -radius * np.cos(theta)
    
    return [x, y]