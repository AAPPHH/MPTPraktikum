import numpy as np
import matplotlib.pyplot as plt

# Beispielhafte Parameter der Verteilung
mu = np.array([2.0, 3.0])  # Erwartungswert
Sigma = np.array([[2.0, 1.2], 
                  [1.2, 1.0]])  # Kovarianzmatrix (nicht-diagonal, d.h. korrelierte Größen)


def plot_covariance_ellipse(mu, Sigma, ax, n_std=1.0, **kwargs):
    """
    **TODO**:
    Zeichnen Sie eine Kovarianzellipse (z. B. 1-, 2- oder 3-Sigma) um den Mittelwert einer 2D-Normalverteilung.
    Verwenden Sie das übergebene `axes <https://matplotlib.org/stable/api/axes_api.html>`_ Objekt zum zeichnen.

    Parameter:
    ----------
    mu : np.ndarray
        2D-Vektor mit dem Mittelwert (Schwerpunkt) der Ellipse.

    Sigma : np.ndarray
        2x2-Kovarianzmatrix der Verteilung.

    ax : matplotlib.axes.Axes
        Achse, in die die Ellipse gezeichnet werden soll.

    n_std : float
        Skalierungsfaktor für die Ellipsenweite (z. B. 1 = 1-Sigma, 2 = 2-Sigma, ...).

    **kwargs :
        Zusätzliche Parameter für `ax.plot`, z. B. Farbe oder Linienstil.
    """
    # TODO: Generieren Sie 100 Punkte auf dem Einheitskreis
    # Verwenden Sie np.linspace um 100 verschiedene Winkel zwischen 0 und 2pi zu bekommen.
    # Wenden Sie dann np.cos und np.sin an und verwenden Sie anschließend np.stack
    # um daraus ein (2, N) Array zu erzeugen. 
    theta = np.linspace(0, 2 * np.pi, 100)
    circle = np.stack((np.cos(theta), np.sin(theta)))  # Shape: (2, N)

    # TODO: Bestimmen Sie die Cholesky-Zerlegung der Kovarianzmatrix Sigma
    # L @ L.T
    L = np.linalg.cholesky(Sigma)

    # TODO: Transformieren Sie den Einheitskreises in eine entsprechende Ellipse
    # Multiplizieren Sie mit n_std um die Ellipse zu skalieren. 
    # Stellen Sie sicher das die Ellipse um den Mittelwert mu zentriert ist.
    ellipse = mu.reshape(2, 1) + n_std * L @ circle

    # Zeichnen Sie die Ellipse in das übergebene ax Objekt.
    # Übergeben Sie die zusätzlichen Parameter in kwargs um das Aussehen der Ellipse
    # beim Aufruf der Methode steuern zu können.
    ax.plot(ellipse[0], ellipse[1], **kwargs)

# ---------------------------------------------------
# There is no need to change anything below this line
# ---------------------------------------------------

if __name__ == "__main__":
  # Stichprobe generieren
  samples = np.random.multivariate_normal(mu, Sigma, size=500)


  # Plot vorbereiten
  fig, ax = plt.subplots(figsize=(6, 6))
  ax.set_aspect('equal')
  ax.grid(True)

  # Datenpunkte darstellen
  ax.scatter(samples[:, 0], samples[:, 1], s=10, alpha=0.3, label="Samples")

  # Erwartungswert markieren
  ax.plot(mu[0], mu[1], 'ro', label="Mittelwert")

  # Kovarianzellipse zeichnen
  plot_covariance_ellipse(mu, Sigma, ax, n_std=1.0, color='#FF0000', label="1-Sigma-Ellipse")
  plot_covariance_ellipse(mu, Sigma, ax, n_std=2.0, color='#CF0000', label="2-Sigma-Ellipse")
  plot_covariance_ellipse(mu, Sigma, ax, n_std=3.0, color='#800000', label="3-Sigma-Ellipse")

  # Achsen und Legende
  ax.set_xlabel("x")
  ax.set_ylabel("y")
  ax.legend()
  plt.title("2D-Normalverteilung mit Kovarianzellipse")
  plt.show()
