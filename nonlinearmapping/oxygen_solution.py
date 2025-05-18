import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

mu, std = 40.0, 5.0  # Mean and standard deviation of oxygen partial pressure (p)


def map_samples(samples):
    """
    **TODO**: Transform samples of a normally distributed oxygen partial pressure (p)
    using the Hill equation to approximate blood oxygen saturation.

    .. math::
        S(p) = \\frac{p^n}{p^n + K^n}

    Note: You need to estimate the mean and variance of the samples by using
    `np.mean <https://numpy.org/doc/2.2/reference/generated/numpy.mean.html>`_ and
    `np.var <https://numpy.org/devdocs/reference/generated/numpy.var.html>`_.

    Additionally compute an analytical approximation of the mean and variance
    of the transformed values via first-order Taylor expansion.

    :param samples:
        A 1D array of sampled oxygen partial pressures (in mmHg), assumed to be
        normally distributed with unknown mean and variance.

    Returns:
    --------
    :return: 3-Tuple of mapped_samples, the estimated mean and the estimated variance of the saturation (via Taylor expansion)
    """
    N, K = 2.7, 26

    # TODO: Apply the Hill function to each sample to get saturation values
    mapped_samples = np.power(samples, N) / (np.power(samples, N) + np.power(K, N))

    # TODO: Use np.mean and np.var to compute mean and variance of the original input samples
    mu = np.mean(samples)
    V = np.var(samples)

    # TODO: Compute the derivative (Jacobian) of the Hill function at the mean
    J = (
        N
        * np.power(K, N)
        * np.power(mu, N - 1)
        / ((np.power(mu, N) + np.power(K, N)) ** 2)
    )

    # TODO: Compute the transformed mean using the Hill function
    mapped_mu = np.power(mu, N) / (np.power(mu, N) + np.power(K, N))

    # TODO: Approximate the transformed variance via linear error propagation
    mapped_var = J * V * J

    # TODO: Return the mapped samples, the mapped mean and the mapped variance
    return mapped_samples, mapped_mu, mapped_var


# ---------------------------------------------------
# There is no need to change anything below this line
# ---------------------------------------------------

# Main Program
if __name__ == "__main__":
    N, K = 2.7, 26

    # Create three plots
    fig, axs = plt.subplots(ncols=3, figsize=(8, 4))

    # Draw random samples for the partial pressure
    p = np.random.normal(mu, std, 10000)

    # Plot histogram and density curve
    df = pd.DataFrame(p, columns=["p"])
    sns.histplot(df, bins=64, ax=axs[0], stat="density")
    x = np.linspace(mu - 5.0 * std, mu + 5.0 * std, 100)
    y = np.exp(-((x - mu) ** 2) / (2 * std**2)) / (std * np.sqrt(2.0 * np.pi))
    axs[0].plot(x, y, color="#1f77b4")
    axs[0].set_title("Sauerstoffpartialdruck - Verteilung")

    # Draw the mapping function itself
    x = np.linspace(0.0, 5.0 * K, 250)
    y, _, _ = map_samples(x)
    axs[1].plot(x, y, color="#1f77b4")
    axs[1].set_ylim(0.0, 1.0)
    axs[1].set_title("Hill-Gleichung")

    # Draw tangent and range which is used from the samples
    y0 = np.power(mu, N) / (np.power(mu, N) + np.power(K, N))
    grad = (
        N
        * np.power(K, N)
        * np.power(mu, N - 1)
        / ((np.power(mu, N) + np.power(K, N)) ** 2)
    )
    y = (x - mu) * grad + y0
    axs[1].plot(x, y, color="orange")
    axs[1].plot(np.array([mu - 3 * std, mu - 3 * std]), np.array([0.0, 1.0]), "k--")
    axs[1].plot(np.array([mu + 3 * std, mu + 3 * std]), np.array([0.0, 1.0]), "k--")

    # Map the samples and retrieve estimated mean and variance
    s, mu, var = map_samples(p)

    # Plot histogram of mapped samples and estimated density
    df = pd.DataFrame(s, columns=["s"])
    sns.histplot(df, bins=64, ax=axs[2], stat="density")
    x = np.linspace(mu - 5.0 * np.sqrt(var), mu + 5.0 * np.sqrt(var), 100)
    y = np.exp(-((x - mu) ** 2) / (2 * var)) / (np.sqrt(2.0 * np.pi * var))
    axs[2].plot(x, y, color="#1f77b4")
    axs[2].set_title("Sauerstoffsättigung - Verteilung")

    axs[2].plot(np.array([mu, mu]), np.array([0.0, np.max(y)]), "k--")

    mu = np.mean(s)
    axs[2].plot(np.array([mu, mu]), np.array([0.0, np.max(y)]), "o--")

    plt.show()
