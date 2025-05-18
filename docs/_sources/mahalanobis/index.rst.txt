Mahalanobis-Distanz und Kovarianzellipsen
=========================================

Die Mahalanobis-Distanz ist ein Maß für den Abstand eines Punkts von einem Mittelwert, das im Gegensatz zur
euklidischen Distanz auch die **Richtung und Streuung der Datenverteilung** berücksichtigt. Sie ist besonders
wichtig für multivariat normalverteilte Zufallsvariablen, bei denen die Variablen **korreliert** und die Skalen
verschieden sein können.

Für eine Zufallsvariable :math:`\boldsymbol{X} \sim \mathcal{N}(\boldsymbol{\mu}, \Sigma)` und einen Punkt
:math:`\boldsymbol{x}` ist die Mahalanobis-Distanz definiert als:

.. math::
   d_M(\boldsymbol{x}) = \sqrt{(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu})}

Diese Distanz ist dimensionslos und normiert die Abweichung entlang jeder Richtung gemäß der
Varianzstruktur der Verteilung. Punkte mit gleicher Mahalanobis-Distanz liegen auf **Ellipsen (2D)** oder
**Ellipsoiden (3D)** um den Erwartungswert.

Kovarianzellipsen
-----------------

Die **Kovarianzellipsen** (in 2D) verbinden all jene Punkte, die zur multivariaten Normalverteilung eine
konstante Mahalanobis-Distanz haben – sie sind also die **Konfidenzbereiche**.

Für eine gegebene Distanz :math:`d` gilt:

.. math::
   \{\boldsymbol{x} \in \mathbb{R}^2 \;|\; d_M(\boldsymbol{x}) = d\}

Die Form und Ausrichtung der Ellipsen wird durch die Kovarianzmatrix :math:`\Sigma` bestimmt:
- Die Hauptachsen entsprechen den **Eigenvektoren** von :math:`\Sigma`.
- Die Längen der Achsen skalieren mit den **Quadratwurzeln der Eigenwerte**.
- Eine größere Varianz entlang einer Richtung → längere Ausdehnung der Ellipse.

Die Ellipsen mit :math:`d_M = 1`, :math:`2`, :math:`3` umfassen etwa 39 %, 86 % bzw. 99 % der
Wahrscheinlichkeit für eine 2D-Gaußverteilung – ähnlich wie die ±1σ-, ±2σ-, ±3σ-Regeln im eindimensionalen Fall.

Diese Ellipsen werden in den folgenden Abbildungen verwendet, um die Streuung und Form multivariater
Zufallsvariablen grafisch darzustellen.

.. image:: ./maha1.png
  :width: 1024px
  :alt: Mahalanobisdistanz
  :align: center

Darstellung von Kovarianzellipsen
---------------------------------

Im eindimensionalen Fall ist der 1-Sigma-Bereich keine Ellipse, sondern besteht aus zwei Punkten:
Man berechnet die Standardabweichung :math:`\sigma = \sqrt{\sigma^2}` aus der Varianz und erhält
die Grenzen des Intervalls durch Addition und Subtraktion vom Mittelwert:

.. math::
   \mu - \sigma \quad \text{und} \quad \mu + \sigma

Dieser Bereich enthält bei einer Normalverteilung etwa 68 % der Wahrscheinlichkeit.

Verallgemeinert man diese Idee auf den mehrdimensionalen Fall, so möchte man ebenfalls die 
„Wurzel“ der Kovarianzmatrix bestimmen, um aus einem **Einheitskreis** (bzw. einer Einheitskugel)
eine gestreckte und rotierte Ellipse (bzw. Ellipsoid) zu erzeugen, die die gleiche Streuung wie 
die gegebene Verteilung aufweist.

Die Matrixwurzel der Kovarianzmatrix :math:`\Sigma` kann über die **Cholesky-Zerlegung** gebildet werden:

.. math::
   \Sigma = LL^\top

Dabei ist :math:`L` eine untere Dreiecksmatrix, die als Transformation dient: 
Wenn :math:`\boldsymbol{z}` eine Zufallsvariable mit :math:`\boldsymbol{z} \sim \mathcal{N}(0, I)` ist, 
dann hat :math:`\boldsymbol{x} = \mu + L \boldsymbol{z}` die Verteilung :math:`\mathcal{N}(\mu, \Sigma)`.

Zur Darstellung einer Kovarianzellipse geht man wie folgt vor:

#. Man erzeugt Punkte :math:`\boldsymbol{z}` auf dem Einheitskreis, z. B. über Winkelparameter :math:`\theta`:

   .. math::
      \boldsymbol{z}(\theta) = 
      \begin{pmatrix}
         \cos(\theta) \\
         \sin(\theta)
      \end{pmatrix}, \quad \theta \in [0, 2\pi)

#. Diese Punkte werden mit der Matrix :math:`L` skaliert und gedreht:

   .. math::
      \boldsymbol{x} = \mu + L \cdot \boldsymbol{z}(\theta)

#. Das Ergebnis ist eine Ellipse, die die Struktur der Kovarianzmatrix repräsentiert.

Je nach gewähltem Skalierungsfaktor (z. B. Radius = 1, 2 oder 3) entsteht eine 1-, 2- oder 3-Sigma-Ellipse, 
die etwa 39 %, 86 % bzw. 99 % der Wahrscheinlichkeit einer 2D-Normalverteilung umfassen.

Diese Darstellung erlaubt eine anschauliche Visualisierung von Unsicherheiten und Korrelationen in mehrdimensionalen 
Verteilungen – insbesondere, wenn man die Wirkung nichtlinearer Transformationen beobachtet.

**Aufgabe 1**: Zeichnen einer Kovarianzellipse
----------------------------------------------

In diesem Praktikum arbeiten Sie in der Datei 

.. code-block:: Python
    
    mahalanobis/maha.py


In dieser Aufgabe sollen Sie lernen, wie man Unsicherheit und Streuung einer zweidimensionalen, 
normalverteilten Zufallsvariable grafisch als **Kovarianzellipse** darstellen kann. 
Dazu implementieren Sie eine Methode, die eine gegebene 2x2-Kovarianzmatrix analysiert und auf Basis 
der Cholesky-Zerlegung eine entsprechende Ellipse in eine bestehende Grafik einträgt.

Die Kovarianzellipse verallgemeinert die Idee der Standardabweichung aus dem eindimensionalen Fall auf 
zwei Dimensionen. Sie beschreibt die Punkte gleicher Mahalanobis-Distanz (z. B. 1-Sigma) um den Erwartungswert 
einer 2D-Normalverteilung. Die Form und Orientierung der Ellipse wird durch die Kovarianzmatrix bestimmt.

Die „Wurzel“ der Kovarianzmatrix wird über die **Cholesky-Zerlegung** gebildet. 

.. math::
   \Sigma = L L^\top

Sie können diese in NumPy
mit der Methode `np.linalg.cholesky <https://numpy.org/doc/2.1/reference/generated/numpy.linalg.cholesky.html>`_ berechnen. 

Die Matrix :math:`L` transformiert den Einheitskreis zu einer Ellipse mit derselben Streuung wie die Normalverteilung.

Implementieren Sie eine nun die Funktion :py:func:`maha.plot_covariance_ellipse`. Folgen Sie den 
Anweisungen im Code sowie dieser Beschreibung.

.. autofunction:: maha.plot_covariance_ellipse

.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

       def plot_covariance_ellipse(mu, Sigma, ax, n_std=1.0, **kwargs):
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


Ändern Sie die Kovarianzmatrix, um zu untersuchen, wie sich Form und Ausrichtung der Ellipsen verändern.

Musterlösung
------------

:doc:`source`