import numpy as np
from funkcije import*
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


# Load the file as a 2D array
data1 = np.loadtxt("mion/output_1.dat")
data2 = np.loadtxt("mion/output_3.dat")

# Split into columns
col1 = data1[:, 0]  # First column
col2 = data1[:, 1]  # Second column
col3 = data2[:, 0]  # First column
col4 = data2[:, 1]  # Second column
N = len(col3)


plt.figure(tight_layout=True)
plt.step(col3, col4)
plt.xlabel("TDC [$\mu s$]")
plt.ylabel("N")
plt.yscale("log")


plt.figure(tight_layout=True)
plt.step(col1, col2)
plt.xlabel("ADC [$V$]")
plt.ylabel("N")
plt.yscale("log")


t = np.linspace(0,9,200)
x_data, y_data = col3[10:-127], col4[10:-127]

# Define the exponential function
def exponential_func(x, a, b, c):
    return a * np.exp(-b*x) + c

# Fit exponential curve
exp_params, exp_cov = curve_fit(exponential_func, x_data, y_data, maxfev=5000)

# Logarithmize the data
log_y_data = np.log(y_data)
print(log_y_data)

# Fit linear function to logarithmized data
def linear_func(x, m, c):
    return m*x + c

lin_params, lin_cov = curve_fit(linear_func, x_data, log_y_data)

# Print parameters and covariance matrices
print("Exponential fit parameters (a, b, c):", exp_params)
print("Exponential covariance matrix:\n", exp_cov)

print("\nLinear fit parameters (m, c):", lin_params)
print("Linear covariance matrix:\n", lin_cov)

# Plotting the results
plt.figure(figsize=(10, 5), tight_layout=True)

# Original data with exponential fit
plt.subplot(1, 2, 1)
plt.step(col3, col4)
plt.plot(t, exponential_func(t, *exp_params), label=r"$\tau=$"+f"{1/exp_params[1]:.2f}$\pm${np.sqrt(1/exp_params[1]**2*exp_cov[1][1]):.3f}")
plt.axvspan(x_data[0], x_data[-1], color="grey", alpha=0.3, label="Fit Region")
plt.xlabel("TDC [$\mu s$]")
plt.ylabel("N")
plt.yscale("log")
plt.legend()


# Logarithmized data with linear fit
plt.subplot(1, 2, 2)
plt.step(col3, np.log(col4))
plt.plot(t, linear_func(t, *lin_params), label=r"$\tau=$"+f"{-1/lin_params[0]:.2f}$\pm${np.sqrt(1/lin_params[0]**2*lin_cov[0][0]):.3f}")
plt.axvspan(x_data[0], x_data[-1], color="grey", alpha=0.3, label="Fit Region")
plt.xlabel("TDC [$\mu s$]")
plt.ylabel("$ln N$")
plt.legend()




# Define a function to plot covariance matrix
def plot_covariance_matrix(cov_matrix, labels, title):
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(cov_matrix, cmap='viridis')
    fig.colorbar(cax)
    
    # Add tick labels
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='left')
    ax.set_yticklabels(labels)
    
    # Annotate with matrix values
    for i in range(cov_matrix.shape[0]):
        for j in range(cov_matrix.shape[1]):
            ax.text(j, i, f"{cov_matrix[i, j]:.2e}", ha='center', va='center', color='black')
    
    # Add title and layout adjustments
    plt.title(title)
    plt.tight_layout()

# Now add fit parameters as an additional legend to your plot (outside of the matrix)
def add_fit_parameters_to_legend(params):
    # param_text_exp = f"$a={exp_params[0]:.2f}, b={exp_params[1]:.2f}, c={exp_params[2]:.2f}$"
    # param_text_lin = f"$m={lin_params[0]:.2f}, c={lin_params[1]:.2f}$"

    handles = [
        plt.Line2D([0], [0], color='none', label=f"Koef.: {params}")
    ]

    # Add second legend for fit parameters
    plt.legend(handles=handles, loc='upper right', fontsize=10, frameon=True)


# Plot covariance matrices
plot_covariance_matrix(
    lin_cov,
    labels=['k', 'n'],
    title="Kovariančna matrika, linfit(logdata)"
)
add_fit_parameters_to_legend(f"$k={lin_params[0]:.2f}, n={lin_params[1]:.2f}$")

plot_covariance_matrix(
    exp_cov,
<<<<<<< HEAD
    labels=['A', r'b=1/$\tau$', 'Offset'],
    title="Kovariančna matrika, expo. fit"
)
add_fit_parameters_to_legend(f"$A={exp_params[0]:.2f}, b={exp_params[1]:.2f}, Offset={exp_params[2]:.2f}$")
=======
    labels=['A', r'$\lambda$=1/$\tau$', 'C'],
    title="Kovariančna matrika, expo. fit"
)
add_fit_parameters_to_legend(f"$A={exp_params[0]:.2f}, \lambda={exp_params[1]:.2f}, C={exp_params[2]:.2f}$")
>>>>>>> kritični


def tau(z, r=5):
    return (1+r)/((1+r) + 0.0000689*z**4)

Z = np.linspace(0,30,100)
plt.figure(tight_layout=True)
for r in [0.5, 1, 2, 5, 10]:
    plt.plot(Z, tau(Z,r), label = f"r={r}")
plt.title("Vpliv scintilatorja")
plt.xlabel("Z")
plt.ylabel(r"$\tau$")
plt.legend()
<<<<<<< HEAD
plt.savefig("mion/slike/relacija_z.png")
=======
#plt.savefig("mion/slike/relacija_z.png")
>>>>>>> kritični

plt.show()


print("\n")
print("Koliko mionov razpade:")
dt = col3[1]-col3[0]
S1 = sum(col4[5:])
ozadje = exp_params[-1]*(N-5)
S2 = S1-ozadje
print("col4[0]:", col4[:5])
print(" z ozadjem - ni upoštevano, bml, \n brez ozadja - ozadje upoštevano, odstranjeno")
print("Nerazpadli detektirani mioni (z ozadjem):", col4[0])
print("Razpadli mioni (z ozadjem):", S1)
print("Razpadli mioni (brez ozadja):", S2)
print("Delež razpadlih glede na vse zaznane (z ozadjem):", S1/sum(col4))
print("Delež razpadlih glede na vse zaznane (minus ozadje):", S2/(sum(col4)-exp_params[-1]*N))
print()
print("Pogostost zaznanih razpadov")
print(f"Začetni čas pet, 13:30, končni pon, 13:00 \n skupaj 3*24h-30min=71,5h={71.5*3600}s")
T = 71*3600 + 1800
print(f"Pogostost (z ozadjem): {S1/T:.3f}s^-1, oz. en mion vsake {T/S1:.3f}s")
print(f"Pogostost (brez ozadja): {S2/T:.3f}s^-1, oz. en mion vsake {T/S2:.3f}s")