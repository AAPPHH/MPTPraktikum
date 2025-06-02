import numpy as np
import cv2
from misc import (
    IMAGE_SHAPE,
    SAMPLES_PER_CLUSTER,
    draw_cluster,
    draw_mahalanobis,
    draw_text,
    draw_axes,
)


def minimum_variance_fusion(mu1, cov1, mu2, cov2):
    """
    **TODO**: Calculate the minimum variance fusion result for
    two normal distributed measurements mu1 and mu2 and their
    respective covariances cov1 and cov2. Return both the fused
    measurement mu as well as the resulting covariance.

    :param mu1: First measurement vector
    :param mu2: Second measurement vector
    :param cov1: Covariance of first measurement
    :param cov2: Covariance of second measurement
    :return: Tuple (mu, cov) containing resulting measurement and covariance of the result.
    """
    inv1 = np.linalg.inv(cov1)
    inv2 = np.linalg.inv(cov2)
    cov = np.linalg.inv(inv1 + inv2)
    mu = cov @ (inv1 @ mu1 + inv2 @ mu2)

    return mu, cov


if __name__ == "__main__":
    # Create a correlated multivariate normal distribution
    mu1 = np.array([0.0, 0.0])
    cov1 = np.array([[1.0, 0.0], [0.0, 1.0]])

    mu2 = np.array([2.0, 2.0])
    cov2 = np.array([[1.0, 0.0], [0.0, 1.0]])

    control = 1

    while True:
        image = np.ones(IMAGE_SHAPE)

        mu, cov = minimum_variance_fusion(mu1, cov1, mu2, cov2)

        cluster1 = np.random.multivariate_normal(mu1, cov1, size=SAMPLES_PER_CLUSTER)
        cluster2 = np.random.multivariate_normal(mu2, cov2, size=SAMPLES_PER_CLUSTER)
        cluster3 = np.random.multivariate_normal(mu, cov, size=SAMPLES_PER_CLUSTER)

        draw_cluster(image, cluster1, col=(0.7, 0.8, 1.0))
        #draw_cluster(image, cluster2, col=(1.00, 0.8, 0.7))
        #draw_cluster(image, cluster3, col=(0.7, 1.0, 0.7))

        draw_mahalanobis(image, mu1, cov1)
        #draw_mahalanobis(image, mu2, cov2, col=(0.92, 0.14, 0.0))
        #draw_mahalanobis(image, mu, cov, col=(0.14, 0.92, 0.14))

        col = (0.6, 0.6, 0.6)
        if control == 1:
            col = (0.0, 0.14, 0.92)
        draw_text(image, mu1, cov1, col=col)

        # col = (0.6, 0.6, 0.6)
        # if control == 2:
        #     col = (0.92, 0.14, 0.0)
        # draw_text(image, mu2, cov2, yOffset=100, col=col)

        # draw_text(image, mu, cov, yOffset=200, col=(0.15, 0.92, 0.14))

        draw_axes(image)
        cv2.imshow("Clusters", image)
        key = cv2.waitKey(0)

        if key == ord("1"):
            control = 1
        if key == ord("2"):
            control = 2

        if key == ord("w"):
            if control == 1:
                mu1[1] += 0.1
            else:
                mu2[1] += 0.1
        if key == ord("s"):
            if control == 1:
                mu1[1] -= 0.1
            else:
                mu2[1] -= 0.1
        if key == ord("a"):
            if control == 1:
                mu1[0] -= 0.1
            else:
                mu2[0] -= 0.1
        if key == ord("d"):
            if control == 1:
                mu1[0] += 0.1
            else:
                mu2[0] += 0.1

        if key == ord("W"):
            if control == 1:
                cov1[1][1] += 0.1
            else:
                cov2[1][1] += 0.1
        if key == ord("S"):
            if control == 1:
                cov1[1][1] -= 0.1
            else:
                cov2[1][1] -= 0.1

        if key == ord("A"):
            if control == 1:
                cov1[0][0] -= 0.1
            else:
                cov2[0][0] -= 0.1
        if key == ord("D"):
            if control == 1:
                cov1[0][0] += 0.1
            else:
                cov2[0][0] += 0.1

        if key == ord("q"):
            if control == 1:
                cov1[0][1] += 0.05
                cov1[1][0] = cov1[0][1]
            else:
                cov2[0][1] += 0.05
                cov2[1][0] = cov2[0][1]
        if key == ord("e"):
            if control == 1:
                cov1[0][1] -= 0.05
                cov1[1][0] = cov1[0][1]
            else:
                cov2[0][1] -= 0.05
                cov2[1][0] = cov2[0][1]

        if key == 27:
            break
