import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Ellipse


# Function to draw covariance ellipse
def draw_cov_ellipse(mean, cov, ax, n_std=2.0, **kwargs):
    # Compute eigenvalues and eigenvectors
    eigvals, eigvecs = np.linalg.eigh(cov)

    # Sort the eigenvalues and corresponding eigenvectors
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    # Compute angle in degrees
    angle = np.degrees(np.arctan2(*eigvecs[:, 0][::-1]))

    # Width and height of ellipse (2*n_std*sqrt(eigenvalue))
    width, height = 2 * n_std * np.sqrt(eigvals)

    # Create and add ellipse to plot
    ellipse = Ellipse(xy=mean, width=width, height=height, angle=angle, **kwargs)
    ax.add_patch(ellipse)


def draw_cov_ellipses(mean, cov, ax, **kwargs):
    for n_std in [1.0, 2.0, 3.0]:
        draw_cov_ellipse(mean, cov, ax, n_std, **kwargs)


def draw_samples(samples, ax):
    df = pd.DataFrame(samples.T, columns=["x", "y"])
    sns.scatterplot(x="x", y="y", data=df, ax=ax)
