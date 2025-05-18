import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Ellipse
from misc import draw_cov_ellipses

N_SAMPLES = 1024


def map_samples(samples):
    x0, x1 = samples[:, 0], samples[:, 1]

    z0 = 0.5 * np.power(x0, 1.4) + 0.9 * np.power(x1, 1.2)
    z1 = 1.2 * np.power(x0, 1.2) + 0.4 * np.power(x1, 1.3)

    return np.stack((z0, z1), axis=1)


def jacobian(mu):
    x0, x1 = mu[0], mu[1]
    return np.array(
        [
            [0.5 * 1.4 * np.power(x0, 0.4), 0.9 * 1.2 * np.power(x1, 0.2)],
            [1.2 * 1.2 * np.power(x0, 0.2), 0.4 * 1.3 * np.power(x1, 0.3)],
        ]
    )


mu = np.array([4.5, 4.5])
cov = np.array([[0.7, -0.4], [-0.4, 1.4]])
samples = np.random.multivariate_normal(mu, cov, size=N_SAMPLES)
mapped_samples = map_samples(samples)

estimated_mu = np.mean(mapped_samples, axis=0)
estimated_cov = np.cov(mapped_samples.T)

calculated_mu = map_samples(mu.reshape(1, -1))[0]
J = jacobian(mu)
calculated_cov = J @ cov @ J.T
# print(estimated_mu, calculated_mu)
# print("\n")
#  print(estimated_cov, "\n", calculated_cov)


sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 6))

df = pd.DataFrame(samples, columns=["x", "y"])
sns.scatterplot(x="x", y="y", data=df, ax=ax)

df = pd.DataFrame(mapped_samples, columns=["x", "y"])
sns.scatterplot(x="x", y="y", data=df, ax=ax)

draw_cov_ellipses(mu, cov, ax, edgecolor="lightblue", facecolor="none", linewidth=2)
draw_cov_ellipses(
    estimated_mu, estimated_cov, ax, edgecolor="orange", facecolor="none", linewidth=2
)
draw_cov_ellipses(
    calculated_mu, calculated_cov, ax, edgecolor="red", facecolor="none", linewidth=2
)

plt.title("Scatter plot of Multivariate Normal Samples")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.xlim(0.0, 15.0)
plt.ylim(0.0, 15.0)
plt.show()
