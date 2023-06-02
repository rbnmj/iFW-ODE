import numpy as np
from scipy import integrate as integ
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from matplotlib.widgets import Slider, Button

class RosenzweigMacArthur:
    # define starting conditions (var0 = densities at start, t = time frame)
    def __init__(self, var0, t):
        self._var0 = var0
        self._t = t

        # call plot function
        self._callplot()

    # define equations for lotka volterra dynamics
    def _equations(self, x, t, r, a, c, d, K, h):
        N = x[0]  # prey
        P = x[1]  # predator

        Ndot = r*(1-N/K)*N - (a*N/(1+a*h*N))*P
        Pdot = c*(a*N/(1+a*h*N))*P - d*P

        return [Ndot, Pdot]

    # plot solutions
    # integrate and write solution into empty list
    def _callplot(self):
        self.fig, self.ax = plt.subplots()
        # set starting parameters
        r0 = 1
        a0 = 0.5
        c0 = 0.25
        d0 = 0.1
        h0 = 1.5
        K0 = 6
        var = []  # empty array for results/densities

        # differential equation, densities at start, time frame, starting values for r, a, c & d
        var = integ.odeint(self._equations, self._var0, self._t,
                           args=(r0, a0, c0, d0, K0, h0))

        self._line1, = self.ax.plot(self._t, var[:, 0], 'g-', label='prey')
        self._line2, = self.ax.plot(self._t, var[:, 1], 'r-', label='predator')
        plt.legend()
        plt.xlabel(r'time')
        plt.ylabel(r'population density')
        plt.ylim(0, 8)
        plt.subplots_adjust(left=0.25, bottom=0.7)
        plt.title("Rosenzweig-MacArthur predator-prey model")

        # adding sliders graphically to change the parameters
        self._rslider = Slider(self.fig.add_axes(
            [0.25, 0.57, 0.65, 0.03]), 'growth rate', 0.0, 5.0, valinit=r0)
        self._dslider = Slider(self.fig.add_axes(
            [0.25, 0.47, 0.65, 0.03]), 'death rate', 0.0, 1.0, valinit=d0)
        self._aslider = Slider(self.fig.add_axes(
            [0.25, 0.37, 0.65, 0.03]), 'attack rate', 0.0, 1, valinit=a0)
        self._cslider = Slider(self.fig.add_axes(
            [0.25, 0.27, 0.65, 0.03]), 'conversion efficiency', 0.0, 0.75, valinit=c0)
        self._Kslider = Slider(self.fig.add_axes(
            [0.25, 0.17, 0.65, 0.03]), 'carrying capacity', 0.0, 10.0, valinit=K0)
        self._hslider = Slider(self.fig.add_axes(
            [0.25, 0.07, 0.65, 0.03]), 'handling time', 0.0, 2.3, valinit=h0)

        # add a reset button graphically
        self.resetbutton = Button(self.fig.add_axes(
            [0.8, 0.02, 0.1, 0.04]), 'Reset', hovercolor='0.9')

        # Values change when the slider is moved and reset everything when Reset is pressed
        graph_exists = True
        if graph_exists:
            self._rslider.on_changed(self._update)
            self._aslider.on_changed(self._update)
            self._cslider.on_changed(self._update)
            self._dslider.on_changed(self._update)
            self._Kslider.on_changed(self._update)
            self._hslider.on_changed(self._update)
            self.resetbutton.on_clicked(self._reset)

    # recalculate densities when slider moves
    def _update(self, val):
        var1 = []
        var1 = integ.odeint(self._equations, self._var0, self._t,
                            args=(self._rslider.val, self._aslider.val, self._cslider.val, self._dslider.val, self._Kslider.val, self._hslider.val))
        self._line1.set_ydata(var1[:, 0])
        self._line2.set_ydata(var1[:, 1])

    # reset all sliders to initial values
    def _reset(self, event):
        self._rslider.reset()
        self._aslider.reset()
        self._cslider.reset()
        self._dslider.reset()
        self._Kslider.reset()
        self._hslider.reset()


if __name__ == "__main__":

    # set starting parameters
    r0 = 1
    a0 = 0.5
    c0 = 0.25
    d0 = 0.1
    h0 = 1.5
    K0 = 6

    # set starting conditions (densities at t0 and time frame)
    interactiveLV = RosenzweigMacArthur([0.1, 0.1], np.arange(0, 1000, 1))

    # display all open figures
    plt.show()
