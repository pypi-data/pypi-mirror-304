
# Flow Regime Map

**FlowRegimeMap** is a Python package to predict flow regimes and plot flow regime maps using the Taitel and Dukler method. It supports both metric and imperial unit inputs.

## Features

- Predicts flow regimes such as Bubble Flow, Slug Flow, Annular Flow, and Dispersed Bubble Flow.
- Plots flow regime maps based on user-defined gas and liquid velocities.
- Supports both metric and imperial unit inputs.

## Installation

You can install the package via pip (after publishing to PyPI):

```bash
pip install flowregimemap
```

## Usage

### Import the Package

First, you need to import the `draw_flow_regime_map_with_imperial` function from the package.

```python
from flowregimemap import draw_flow_regime_map_with_imperial
```

### Example Usage

Here’s how to use the function with the provided example parameters:

```python
# Import the function
from flowregimemap import draw_flow_regime_map_with_imperial

# Example inputs in imperial units
rho_L_imperial = 62.4  # Liquid density in lb/ft³
rho_G_imperial = 0.0801  # Gas density in lb/ft³
mu_imperial = 0.89  # Liquid viscosity in cP
sigma_imperial = 70  # Surface tension in dyne/cm
D_imperial = 2  # Pipe diameter in inches

# Example inputs for operating point in imperial units
U_LS_imperial = 3  # Superficial liquid velocity in ft/s
U_GS_imperial = 3  # Superficial gas velocity in ft/s

# Call the function to generate the flow regime map
draw_flow_regime_map_with_imperial(rho_L_imperial, rho_G_imperial, sigma_imperial, mu_imperial, D_imperial, U_GS_imperial, U_LS_imperial)
```

This function will generate a plot of the flow regime map and indicate the operating point.

### Parameters

- `rho_L_imperial`: Liquid density (lb/ft³)
- `rho_G_imperial`: Gas density (lb/ft³)
- `mu_imperial`: Viscosity (cP)
- `sigma_imperial`: Surface tension (dyne/cm)
- `D_imperial`: Pipe diameter (inches)
- `U_LS_imperial`: Superficial liquid velocity (ft/s)
- `U_GS_imperial`: Superficial gas velocity (ft/s)

### Output

- A log-log plot showing various flow regimes and the operating point based on the given parameters.

### Dependencies

- `numpy`
- `matplotlib`

Make sure to install the required dependencies by running:

```bash
pip install numpy matplotlib
```
