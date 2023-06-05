import numpy as np
from scipy import integrate as integ
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from matplotlib.widgets import Slider, Button, RadioButtons
from ModelLib.LV import LotkaVolterra
from ModelLib.RM import RosenzweigMacArthur
from ModelLib.FoodWeb import FoodWeb

class FullWidget:
    def __init__(self):
        self.model_selection_axes = plt.axes([0.1, 0.7, 0.2, 0.15])
        self.model_selection_radios = RadioButtons(self.model_selection_axes, 
                                                   ["Lotka-Volterra Predator Prey", 
                                                    "Rosenzweig-MacArthur Predator Prey",
                                                    "Food Web Model"])
        self.model_selection_radios.on_clicked(self.run_model)

    def run_model(self, modeltype):
        if modeltype == "Rosenzweig-MacArthur Predator Prey":
            #plt.close("all")
            RosenzweigMacArthur([0.1, 0.1], np.arange(0, 1000, 1))
            plt.show()
        elif modeltype == "Lotka-Volterra Predator Prey":
            #plt.close("all")
            LotkaVolterra([0.5, 1.], np.arange(0, 100, 1))
            plt.show()
        elif modeltype == "Food Web Model":
            #plt.close("all")
            FoodWeb([2, 2.5, 2.5, 2, 0.08, 0.4, 0.05, 0.1], np.arange(0, 1000, 1))
            plt.show()


if __name__ == '__main__':
    myApp = FullWidget()
    plt.show()