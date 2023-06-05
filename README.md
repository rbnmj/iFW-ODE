# iPM-ODE
iPM-ODE is a simple Python applet for interactive use of population models based on differential equations. Important model parameters can be modified on the fly and updated simulation results are displayed in real time.  
The applet is still very much a work in progress but completely functional for Lotka-Volterra, Rosenzweig-Macarthur and for one example of a more extended food web.  
iPM-ODE is designed for research and education simultaneously and extension of the app with custom models is very straightforward.

# Requirements 
iPM-ODE is written in Python 3.11 and only requires the packages [numpy](https://numpy.org/), [scipy](https://scipy.org/), and [matplotlib](https://matplotlib.org/) to run.

# Usage
Simply running `iPM-ODE.py` will show a model selector. Selecting a model will open the corresponding interactive time series. Important parameters can be modified via sliders or text boxes and time series will adjust automatically.

Alternatively, standalone models can be run directly from `/StandaloneModels/`, bypassing the model selector. While this offers no additional functionality, it is helpful for quick access to the model library.
