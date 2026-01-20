import numpy as np
from funkcije import*
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


# MONTE CARLO SIM
# Generate n uniform samples
n = 170000
uniform_samples = np.random.uniform(0, 1, n)

# Transform to exponential with lambda=2
lambda_param = 2.02
exp_samples0 = -4*np.log(1 - uniform_samples) / lambda_param

# Generate 1000 samples with scale=2
exp_samples = 4.1*np.random.exponential(scale=1/lambda_param, size=n)




# Lambda=3, generate 1000 samples
poiss_samples = np.random.poisson(lam=1, size=n)



# Load the file as a 2D array
data1 = np.loadtxt("mion/output_1.dat")
data2 = np.loadtxt("mion/output_3.dat")

# Split into columns
col1 = data1[:, 0]  # First column
col2 = data1[:, 1]  # Second column
col3 = data2[:, 0]  # First column
col4 = data2[:, 1]  # Second column
N = len(col3)


x_data, y_data = col3[10:-527], col4[10:-527]

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


# Print parameters and covariance matrices
print("Exponential fit parameters (a, b, c):", exp_params)
print("Exponential covariance matrix:\n", exp_cov)




plt.figure(tight_layout=True)
plt.step(col3, col4)
plt.hist(exp_samples0, bins=col3)
plt.hist(exp_samples, bins=col3, alpha=0.4)
alpha = 4
plt.hist(alpha*8.2*uniform_samples, bins=col3, alpha=0.4)
plt.xlim(-0.5,8.2)
plt.xlabel("TDC [$\mu s$]")
plt.ylabel("N")
plt.yscale("log")


hist0, bins0 = np.histogram(alpha*8.2*uniform_samples, bins=col3)
hist1, bins1 = np.histogram(exp_samples0, bins=col3)
hist2, bins2 = np.histogram(exp_samples, bins=col3)

pars0, covs0 = curve_fit(exponential_func, bins0[:-1], hist2, maxfev=5000)
pars1, covs1 = curve_fit(exponential_func, bins1[:-1], hist1, maxfev=5000)
pars2, covs2 = curve_fit(exponential_func, bins0[:-1], hist0+hist1, maxfev=5000)

plt.figure(tight_layout=True)
plt.step(col3, col4)
plt.step(col3[:-1], hist1)
plt.step(col3[:-1], hist2)
plt.step(col3[:-1], hist0+hist1)
t = np.linspace(-0.5,8.2, 200)
plt.plot(t, exponential_func(t, *exp_params), label=r"$\tau=$"+f"{1/exp_params[1]:.2f}$\pm${np.sqrt(1/exp_params[1]**2*exp_cov[1][1]):.3f}")
plt.plot(t, exponential_func(t, *pars0), label=r"$\tau=$"+f"{1/pars0[1]:.2f}$\pm${np.sqrt(1/pars0[1]**2*covs0[1][1]):.3f}")
plt.plot(t, exponential_func(t, *pars1), label=r"$\tau=$"+f"{1/pars1[1]:.2f}$\pm${np.sqrt(1/pars1[1]**2*covs1[1][1]):.3f}")
plt.plot(t, exponential_func(t, *pars2), label=r"$\tau=$"+f"{1/pars2[1]:.2f}$\pm${np.sqrt(1/pars2[1]**2*covs2[1][1]):.3f}")
plt.axvspan(x_data[0], x_data[-1], color="grey", alpha=0.3, label="Fit Region")
plt.xlim(-0.3,8.2)
plt.xlabel("TDC [$\mu s$]")
plt.ylabel("N")
plt.yscale("log")
plt.legend()




plt.show()



