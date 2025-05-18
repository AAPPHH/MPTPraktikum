import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from misc import draw_samples, draw_cov_ellipses


def map_samples(samples, alpha):
    """
    **TODO**
    Assume you have a normal distributed random variable :math:`\\boldsymbol{X}`
    with mean

    .. math::
      \mu = (1.5 ,0.5)

    and covariance

    .. math::
      \Sigma = \\begin{pmatrix}0.7&-0.4\\\\-0.4&1.4\\end{pmatrix}

    Assume further that :math:`\\boldsymbol{Y}` is another random variable with

    .. math::
      \\boldsymbol{Y} = A\cdot \\boldsymbol{X}

    and

    .. math::
      A = \\begin{pmatrix}\cos(\\alpha)&-\sin(\\alpha)\\\\\sin(\\alpha)&\cos(\\alpha)\\end{pmatrix}

    The samples parameter holds 512 samples of this random variable.

    Apply the linear mapping to the samples and calculate the **exact** new mean and covariance of
    :math:`\\boldsymbol{Y}`, namely

    .. math::
      E[\\boldsymbol{Y}] = E[A\cdot\\boldsymbol{X}] = A\cdot\\boldsymbol{\mu}

    .. math::
      Cov[\\boldsymbol{Y}] = Cov[A\cdot\\boldsymbol{X}] = A\cdot Cov[\\boldsymbol{X}] \cdot A^T

    Return the mapped samples as well as the
    *exact* mean and covariance of the mapped random variable.
    **Do not** estimate the mean and covariance from the mapped samples.

    :param samples: (np.array 2x512) 512 Samples from :math:`\\boldsymbol{X}`
    :param alpha: Parameter :math:`\\alpha` of the Matrix :math:`A` (see above)
    :return: 3-tuple (mapped_samples, mapped_mu, mapped_cov)
    """
    # TODO: Calculate Matrix A

    # TODO: Map the samples and calculate the exact mean and covariance of the Y

    # TODO: Return your mapped samples, the mapped mean and the mapped covariance
    pass


# ---------------------------------------------------
# There is no need to change anything below this line
# ---------------------------------------------------

# Generate 512 samples of a multivariate normal random variable (Shape 2 x 512)
# Do not change
samples = np.random.multivariate_normal(
    mean=np.array([1.5, 0.5]), cov=np.array([[0.7, -0.4], [-0.4, 1.4]]), size=512
).T

# Main Program
if __name__ == "__main__":
    # Set Seaborn display style
    sns.set_style("whitegrid")

    # Create figure for plots
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 8))

    # Iterate different radians for plotting (0 to 2pi)
    for radians in np.linspace(0.0, 2.0 * np.pi, 360):
        # Clear all axes
        for a in ax:
            a.clear()

        # Generate mapped samples
        mapped_samples, mapped_mu, mapped_cov = map_samples(samples, radians)

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
        for cnt in [0, 1]:
            if cnt == 0:
                ax[cnt].set_title("Linear Mapping - Original Data")
            else:
                ax[cnt].set_title("Linear Mapping - Wrapped Grid")

            ax[cnt].set_xlabel("x0")
            ax[cnt].set_ylabel("x1")
            ax[cnt].set_xlim(-6.0, 6.0)
            ax[cnt].set_ylim(-6.0, 6.0)
            ax[cnt].set_aspect("equal")

        # Wait shortly for animation to roll
        plt.pause(0.01)
