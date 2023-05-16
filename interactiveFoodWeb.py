import numpy as np
from scipy import integrate as integ
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from matplotlib.widgets import Slider, Button, TextBox


class LotkaVolterra:
    # define starting conditions (var0 = densities at start, t = time frame)
    def __init__(self, var0, t):
        self._var0 = var0
        self._t = t

        # call plot function
        self._callplot()

    # define equations for lotka volterra dynamics
    def _equations(self, var, t, d_Hmax1, d_Hmax2, k_1, k_2):
        # fill var
        N_a = var[0]
        N_b = var[1]
        A_a = var[2]
        A_b = var[3]
        H_1a = var[4]
        H_1b = var[5]
        H_2a = var[6]
        H_2b = var[7]

        # growth rate of autotrophs
        r_a = (r_max * N_a) / (N_h + N_a)
        r_b = (r_max * N_b) / (N_h + N_b)

        # growth rate of competitors
        g_1a = (a_1 * A_a) / (1 + a_1 * h * A_a)
        g_1b = (a_1 * A_b) / (1 + a_1 * h * A_b)
        g_2a = (a_2 * A_a) / (1 + a_2 * h * A_a)
        g_2b = (a_2 * A_b) / (1 + a_2 * h * A_b)

        # inflection points
        x_01 = D / (a_1 * (e - h * D))
        x_02 = D / (a_2 * (e - h * D))

        # dispersal rates of competitors
        d_H1a = d_Hmax1 / (1 + np.exp(k_1 * (A_a - x_01)))
        d_H1b = d_Hmax1 / (1 + np.exp(k_1 * (A_b - x_01)))
        d_H2a = d_Hmax2 / (1 + np.exp(k_2 * (A_a - x_02)))
        d_H2b = d_Hmax2 / (1 + np.exp(k_2 * (A_b - x_02)))

        # change of nutrients
        dN_a = D * (S - N_a) - r_a * A_a + d_N * (N_b - N_a)
        dN_b = D * (S - N_b) - r_b * A_b + d_N * (N_a - N_b)

        # change of autotrophs
        dA_a = r_a * A_a - ((g_1a * H_1a) + (g_2a * H_2a)) - \
            D * A_a + d_A * (A_b - A_a)
        dA_b = r_b * A_b - ((g_1b * H_1b) + (g_2b * H_2b)) - \
            D * A_b + d_A * (A_a - A_b)

        # change of competitors
        dH_1a = e * g_1a * H_1a - D * H_1a - d_H1a * H_1a + d_H1b * H_1b
        dH_1b = e * g_1b * H_1b - D * H_1b - d_H1b * H_1b + d_H1a * H_1a
        dH_2a = e * g_2a * H_2a - D * H_2a - d_H2a * H_2a + d_H2b * H_2b
        dH_2b = e * g_2b * H_2b - D * H_2b - d_H2b * H_2b + d_H2a * H_2a

        return (dN_a, dN_b, dA_a, dA_b, dH_1a, dH_1b, dH_2a, dH_2b)

    # plot solutions
    # integrate and write solution into empty list
    def _callplot(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_facecolor('whitesmoke')
        self.fig.set_facecolor('whitesmoke')
        var = []  # empty array for results/densities

        # differential equation, densities at start, time frame, starting values for r, a, c & d
        var = integ.odeint(self._equations, self._var0, self._t,
                           args=(d_Hmax1, d_Hmax2, k_1, k_2))

        self._line1, = self.ax.plot(
            self._t, var[:, 4], '-', color="#FF7F0E", label='patch1')
        self._line2, = self.ax.plot(
            self._t, var[:, 5], '-', color="#1F77B4", label='patch2')
        self._line3, = self.ax.plot(self._t, var[:, 6], '-', color="#FFA500")
        self._line4, = self.ax.plot(self._t, var[:, 7], '-', color="#00BFFF")
        # plt.legend()
        plt.xlabel(r'time')
        plt.ylabel(r'population density')
        plt.ylim(0, 0.6)
        plt.xlim(0, 1000)
        plt.subplots_adjust(left=0.25, bottom=0.7)
        plt.title("")

        # add sliders
        self._k1slider = Slider(self.fig.add_axes(
            [0.25, 0.37, 0.65, 0.03]), 'k1', 0.0, 2.0, valinit=0)
        self._k2slider = Slider(self.fig.add_axes(
            [0.25, 0.32, 0.65, 0.03]), 'k2', 0.0, 2.0, valinit=0)

        self._d1textbox = TextBox(self.fig.add_axes(
            [0.25, 0.52, 0.1, 0.03]), 'dHmax1', initial='10')
        self._d2textbox = TextBox(self.fig.add_axes(
            [0.25, 0.47, 0.1, 0.03]), 'dHmax2', initial='0.01')

        # add a reset button graphically
        self.resetbutton = Button(self.fig.add_axes(
            [0.625, 0.47, 0.1, 0.04]), 'Reset', hovercolor='0.9')

        self.updatebutton = Button(self.fig.add_axes(
            [0.5, 0.47, 0.1, 0.04]), 'Update', hovercolor='0.9')

        # Values change when the slider is moved and reset everything when Reset is pressed
        graph_exists = True
        if graph_exists:
            self._k1slider.on_changed(self._update)
            self._k2slider.on_changed(self._update)
            self.resetbutton.on_clicked(self._reset)
            self.updatebutton.on_clicked(self._update)
            # self._text_box.on_submit(self._update)

    # recalculate densities when slider moves

    def _update(self, val):
        dhmax1float = float(self._d1textbox.text)
        dhmax2float = float(self._d2textbox.text)
        var1 = []
        var1 = integ.odeint(self._equations, self._var0, self._t,
                            args=(dhmax1float, dhmax2float, self._k1slider.val, self._k2slider.val))
        self._line1.set_ydata(var1[:, 4])
        self._line2.set_ydata(var1[:, 5])
        self._line3.set_ydata(var1[:, 6])
        self._line4.set_ydata(var1[:, 7])

    # reset all sliders to initial values
    def _reset(self, event):
        self._k1slider.reset()
        self._k2slider.reset()
        self._d1textbox.set_val('10')
        self._d2textbox.set_val('0.01')


if __name__ == "__main__":
    # set parameters
    S = 4.8  # Nutrient supply concentration
    D = 0.3  # Dilution rate
    N_h = 1.5  # half saturation constant for nutrient uptake
    r_max = 0.7  # growth rate of autotroph
    h = 0.53  # handling time
    e = 0.33  # conversion efficiency of competitor
    d_N = 1  # Dispersal rate of nutrients
    d_A = 0.001  # dispersal rate of autotrophs

    # competitiveness
    a_1 = 1  # attack rate of competitor 1
    a_2 = 1  # attack rate of competitor 2

    # adaptability
    k_1 = 0  # dispersal adaptability of competitor 1
    k_2 = 0  # dispersal adaptability of competitor 2
    # 0 = random dispersal, 2 = adaptive dispersal

    # dispersal speed
    d_Hmax1 = 10  # maximal dispersal rates of competitor 1
    d_Hmax2 = 0.01  # maximal dispersal rates of competitor 2

    # time series
    t_end = 400
    number_steps = 20000
    t = np.linspace(0, t_end, number_steps)

    # set starting conditions (densities at t0 and time frame)
    interactiveLV = LotkaVolterra(
        [2, 2.5, 2.5, 2, 0.08, 0.4, 0.05, 0.1], np.arange(0, 1000, 1))

    # display all open figures
    plt.show()
