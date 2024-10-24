import numpy as np
import matplotlib.pyplot as plt

# Function to predict the flow regime and plot the combined curve with the operating point
def predict_flow_regime(U_GS_operating, U_LS_operating, U_GS_E, curve_B_adjusted, curve_C_adjusted, U_GS,
                        curve_A_adjusted):
    # Combine curve_B and curve_C adjusted (they are defined in different ranges)
    combined_curve = np.where(np.isnan(curve_B_adjusted), curve_C_adjusted, curve_B_adjusted)

    # Check if U_GS_operating is greater than U_GS_E (Annular flow condition)
    if U_GS_operating > U_GS_E:
        return "Annular Flow"

    # Filter out NaN values from curve_A_adjusted and combined_curve
    valid_idx_combined = ~np.isnan(combined_curve)


    combined_curve_valid = combined_curve[valid_idx_combined]

    U_GS_valid_combined = U_GS[valid_idx_combined]

    # Find the nearest U_GS value in the defined range
    idx_nearest_gs = (np.abs(U_GS_valid_combined - U_GS_operating)).argmin()  # Index of nearest U_GS

    # Get the corresponding combined curve value at the nearest U_GS
    U_LS_nearest = combined_curve[idx_nearest_gs]

    # Check if U_LS_operating is greater than the combined curve value at the nearest U_GS
    if U_LS_operating > U_LS_nearest:
        return "Dispersed Bubble"

    # If curve_A_adjusted is None, return Slug Flow
    if curve_A_adjusted is None:
        return "Slug Flow"

    valid_idx_a = ~np.isnan(curve_A_adjusted)
    curve_A_valid = curve_A_adjusted[valid_idx_a]
    U_GS_valid_A = U_GS[valid_idx_a]
    # Find the nearest point on curve_A_adjusted to the operating U_LS, ignoring NaNs
    idx_nearest_a = (np.abs(curve_A_valid - U_LS_operating)).argmin()  # Nearest index on Curve A

    # Get the corresponding U_GS value at the nearest point on curve A
    U_GS_nearest_A = U_GS_valid_A[idx_nearest_a]  # Nearest U_GS in Curve A

    # Compare the operating U_GS to the nearest U_GS from Curve A
    if U_GS_operating > U_GS_nearest_A:
        return "Slug Flow"

    # If none of the above, it is Bubble Flow
    return "Bubble Flow"



def convert_to_metric(rho_L_imperial, rho_G_imperial,
                      sigma_imperial, mu_imperial,
                      D_imperial,
                      U_GS_imperial, U_LS_imperial):
    lbft3_to_kgm3 = 16.0185  # 1 lb/ft³ = 16.0185 kg/m³
    dyne_cm_to_N_m = 0.001  # 1 dyne/cm = 0.001 N/m
    inches_to_meters = 0.0254  # 1 inch = 0.0254 meters
    ftsec_to_msec = 0.3048  # 1 ft/s = 0.3048 m/s
    centipoise_to_pascal_sec = 0.001  # 1 cP = 0.001 Pa.s (dynamic viscosity)
    # Convert inputs to metric units
    rho_L_metric = rho_L_imperial * lbft3_to_kgm3
    rho_G_metric = rho_G_imperial * lbft3_to_kgm3
    sigma_metric = sigma_imperial * dyne_cm_to_N_m
    D_metric = D_imperial * inches_to_meters
    U_GS_metric = U_GS_imperial * ftsec_to_msec
    U_LS_metric = U_LS_imperial * ftsec_to_msec

    # Kinematic viscosity (ν) = dynamic viscosity (μ) / density (ρ)
    mu_L_metric = mu_imperial * centipoise_to_pascal_sec  # dynamic viscosity in Pa.s
    nu_L_metric = mu_L_metric / rho_L_metric  # kinematic viscosity in m²/s

    return rho_L_metric, rho_G_metric, sigma_metric, nu_L_metric, D_metric, U_GS_metric, U_LS_metric


# Function to draw the flow regime map
def draw_flow_regime_map(rho_L, rho_G, sigma,nu, D, U_GS_operating, U_LS_operating):
    # Variables:
    # g: Acceleration due to gravity in m/s^2
    # rho_L: Liquid density in kg/m^3
    # rho_G: Gas density in kg/m^3
    # sigma: Surface tension in N/m
    # nu: Kinematic Viscosity in m2/s
    # D: Pipe diameter in meters
    # U_GS_operating: Superficial gas velocity (operating point) in m/s
    # U_LS_operating: Superficial liquid velocity (operating point) in m/s

    # Create an array of superficial gas velocities (U_GS) with 1000 steps for finer resolution
    g = 9.81
    U_GS = np.logspace(-3, 3, 1000)

    # Calculate constants used in equations for Curve A, B, C, and E
    term_A = 1.15 * (g * (rho_L - rho_G) * sigma / (rho_L ** 2)) ** 0.25
    term_B = 4.0 * ((D ** 0.429) * (sigma / rho_L) ** 0.089 / (nu ** 0.072)) * ((g * (rho_L - rho_G) / rho_L) ** 0.446)

    # Curve B: U_LS + U_GS = term_B
    curve_B = term_B - U_GS

    # Curve C: U_GS = 3.17 U_LS
    curve_C = U_GS / 3.17

    # Adjust Curve C: only plot points where Curve C is greater than Curve B and stop at Curve E
    U_GS_E = 3.1 * ((sigma * g * (rho_L - rho_G)) ** 0.25) / (rho_G ** 0.5)
    # Adjust Curve B: only plot points where Curve B is greater than Curve C and less than E
    curve_B_adjusted = np.where((curve_B > curve_C) & (U_GS < U_GS_E), curve_B, np.nan)

    curve_C_adjusted = np.where((curve_C > curve_B) & (U_GS < U_GS_E), curve_C, np.nan)

    # Curve A condition from Equation (14)
    condition_A = (rho_L ** 2 * g * D ** 2 / ((rho_L - rho_G) * sigma)) ** 0.25 >= 4.36

    # If the condition for Curve A is satisfied, calculate Curve A
    if condition_A:
        curve_A = 3.0 * U_GS - term_A
        # Adjust Curve A: only plot points where Curve A is less than Curve B (not the adjusted version of Curve B)
        curve_A_adjusted = np.where((curve_A < curve_B) & (U_GS < U_GS_E), curve_A, np.nan)
    else:
        curve_A_adjusted = None
        print("Condition for Curve A is not met. Curve A will not be drawn.")

    flow_regime = predict_flow_regime(U_GS_operating, U_LS_operating, U_GS_E, curve_B_adjusted, curve_C_adjusted, U_GS,
                                      curve_A_adjusted)

    # Plot the curves in log-log scale
    plt.figure(figsize=(8, 6))

    # Plot Curve A (Bubble to Slug) only if condition is met
    if curve_A_adjusted is not None:
        plt.plot(U_GS, curve_A_adjusted, label="Curve A (Bubble to Slug Transition)", color='b')

    # Plot Curve B (Turbulent Dispersion Limit) adjusted
    plt.plot(U_GS, curve_B_adjusted, label="Curve B (Dispersed Bubble Limit)", color='r')

    # Plot Curve C (Void Fraction Limit) adjusted
    plt.plot(U_GS, curve_C_adjusted, label="Curve C (Dispersed Bubble Limit)", color='g')

    # Plot Corrected Curve E (Transition to Annular Flow)
    plt.axvline(x=U_GS_E, color='m', label="Curve E Annular Flow Transition")

    # Plot the operating point
    plt.plot(U_GS_operating, U_LS_operating, 'o', label=f'Operating Point, flow regime {flow_regime}', markersize=8, color='black')

    # Set log-log scale and limits
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([0.001, 1000])
    plt.ylim([0.001, 1000])

    # Add labels and legend
    plt.xlabel('Superficial Gas Velocity (U_GS) [m/s]')
    plt.ylabel('Superficial Liquid Velocity (U_LS) [m/s]')
    plt.title('Taitel and Dukler Flow Regime Map with Operating Point')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.show()


# New function to draw the map using imperial inputs
def draw_flow_regime_map_with_imperial(rho_L_imperial, rho_G_imperial, sigma_imperial,mu_imperial,
                                       D_imperial, U_GS_imperial,U_LS_imperial):
    # Variables:
    # rho_L_imperial: Liquid density in lb/ft^3
    # rho_G_imperial: Gas density in lb/ft^3
    #mu_imperial in cp
    # sigma_imperial: Surface tension in dyne/cm
    # D_imperial: Pipe diameter in inches
    # U_GS_imperial: Superficial gas velocity in ft/sec
    # U_LS_imperial: Superficial liquid velocity in ft/sec

    # Convert the inputs to metric units
    rho_L_metric, rho_G_metric, sigma_metric, nu_metric,D_metric, U_GS_metric, U_LS_metric =\
        convert_to_metric(rho_L_imperial,rho_G_imperial,sigma_imperial,mu_imperial,D_imperial,U_GS_imperial,U_LS_imperial)
    # Use the converted metric inputs to draw the flow regime map with the operating point
    draw_flow_regime_map(rho_L=rho_L_metric, rho_G=rho_G_metric,
                         sigma= sigma_metric,
                         nu= nu_metric,
                         D=D_metric,
                         U_GS_operating=U_GS_metric,U_LS_operating= U_LS_metric)

