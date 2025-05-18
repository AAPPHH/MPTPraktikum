import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from misc import draw_samples, draw_cov_ellipses

STD_ALPHA = 5  # Standard deviation of angular values (degrees)


def map_samples(samples, radius, alpha, cov):
    """
  **TODO** 
  Assume you have a normal distributed random variable :math:`\\boldsymbol{X}`
  with mean 
  
  .. math::
    \mu = (r, \\alpha) 
    
  and given covariance (`cov`-Parameter). :math:`\\boldsymbol{X}` represents
  a random point in polar coordinates. We want to transform that point into cartesian coordinates by 
  applying the following transformation

  .. math::
    \\boldsymbol{Y} = \\begin{pmatrix}
      r\cdot\cos(\\alpha)\\\\
      r\cdot\sin(\\alpha)
    \\end{pmatrix}

  The samples parameter holds 512 samples of this random variable.

  Apply the non-linear mapping to the samples and calculate the **exact** new mean and covariance of
  :math:`\\boldsymbol{Y}` after linearization using the Jacobian Matrix ::math:`J`, namely

  .. math::
    E[\\boldsymbol{Y}] = f(\\boldsymbol{\mu})

  .. math::
    Cov[\\boldsymbol{Y}] = J\cdot Cov[\\boldsymbol{X}] \cdot J^T

  Return the mapped samples as well as the 
  derived mean and covariance of the mapped random variable. 
  **Do not** estimate the mean and covariance from the mapped samples.

  :param samples: (np.array 2x512) 512 Samples from :math:`\\boldsymbol{X}`
  :param radius: The mean radius in polar coordinates
  :param alpha: The mean angle in polar coordinates
  :return: 3-tuple (mapped_samples, mapped_mu, mapped_cov)
  """
    # TODO: Map all samples from polar to cartesian coordinates
    r, a = samples[0, :], samples[1, :]

    mapped_samples = np.zeros_like(samples)
    mapped_samples[0, :] = r * np.cos(a)
    mapped_samples[1, :] = r * np.sin(a)

    # TODO: Calculate Jacobian
    J = np.array(
        [
            [np.cos(alpha), -radius * np.sin(alpha)],
            [np.sin(alpha), radius * np.cos(alpha)],
        ]
    )

    # TODO: Calculate mean and covariance of Y after linearization
    mapped_mu = np.array([radius * np.cos(alpha), radius * np.sin(alpha)])
    mapped_cov = J @ cov @ J.T

    # TODO: Return your mapped samples, the mapped mean and the mapped covariance
    return mapped_samples, mapped_mu, mapped_cov


# ---------------------------------------------------
# There is no need to change anything below this line
# ---------------------------------------------------

# Main Program
if __name__ == "__main__":
    # Set Seaborn display style
    sns.set_style("whitegrid")

    # Create figure for plots
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 8))

    # Iterate different radians for plotting (0 to 2pi)
    for radians in np.linspace(-np.deg2rad(45), np.deg2rad(45), 90):
        # Generate 512 samples of a multivariate normal random variable (Shape 2 x 512)
        cov = np.array([[0.5, 0.0], [0.0, np.deg2rad(STD_ALPHA) ** 2]])

        samples = np.random.multivariate_normal(
            mean=np.array([50, radians]), cov=cov, size=512
        ).T

        # Clear all axes
        for a in ax:
            a.clear()

        # Generate mapped samples
        mapped_samples, mapped_mu, mapped_cov = map_samples(samples, 50.0, radians, cov)

        # Estimate mu and covariance from original samples as well as mapped samples
        mu = np.mean(samples, axis=1)
        cov = np.cov(samples)

        estimated_mu = np.mean(mapped_samples, axis=1)
        estimated_cov = np.cov(mapped_samples)

        # Draw original sample point cloud as well as mapped samples point cloud
        draw_samples(samples, ax[0])
        draw_samples(mapped_samples, ax[1])

        # Draw covariance ellipses
        draw_cov_ellipses(
            mu, cov, ax[0], edgecolor="lightblue", facecolor="none", linewidth=2
        )
        draw_cov_ellipses(
            estimated_mu,
            estimated_cov,
            ax[1],
            edgecolor="lightblue",
            facecolor="none",
            linewidth=2,
        )
        draw_cov_ellipses(
            mapped_mu,
            mapped_cov,
            ax[1],
            edgecolor="#1f77b4",
            facecolor="none",
            linewidth=2,
        )

        # Apply styling to plot
        ax[0].set_title("Polar Coordinates")
        ax[1].set_title("Cartesian Coordinates")

        ax[0].set_xlabel("r")
        ax[0].set_ylabel("alpha")
        ax[0].set_xlim(20.0, 80.0)
        ax[0].set_ylim(-np.deg2rad(60), np.deg2rad(60))

        ax[1].set_xlim(20.0, 80.0)
        ax[1].set_ylim(-45.0, 45.0)

        # Wait shortly for animation to roll
        plt.pause(0.1)
        # plt.show()
