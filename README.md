# iPM-ODE
iPM-ODW is a simple Python applet to use with population models based on differential equations. Important model parameters can be modified on the fly by updating simulation results.  
The applet is still very much a work in progress but completely functional for Lotka-Volterra (`interactiveLV.py`), Rosenzweig-Macarthur (`interactiveRM.py`) and one example for a more extended food web (`interactiveFoodWeb.py`).  
iPM-ODE is designed for research and education simultaneously and the extension of the app with custom models is very straightforward.

# Requirements 
iPM-ODE is written in Python 3.11 and requires the following packages:
- numpy
- scipy
- matplotlib

# Usage
Simply running `iPM-ODE.py` will show a model selector. Selecting a model will open the corresponding interactive time series. Important parameters can be modified via sliders and text boxes and time series will adjust automatically.

Alternatively, standalone models can be run directly, bypassing the model selecter. This offers no additional functionality it is rather used as an model archive.