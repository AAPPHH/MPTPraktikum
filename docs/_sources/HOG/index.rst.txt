Histogram of Oriented Gradients
===============================

Bei den s.g. HoG (Histogram of Oriented Gradients) Featuren handelt es sich um eine frühe 
Technik aus einem Bild geeigente Informationen (Features) abzuleiten 
um damit komplexe Objekte klassifizeiren zu können. Konkret wurden HOG-Features 
zuerst von N. Dalal und B. Triggs in `Histograms of oriented gradients for human detection, IEEE 2005 <https://ieeexplore.ieee.org/document/1467360>`_
vorgeschlagen. 

HoG - Überblick
---------------
Zunächst werden für das Bild mit dem Sobel-Operator die Gradienten in X und Y-Richtung bestimmt. 
Es wird eine feste Anzahl an möglichen Gradientenrichtungen (z.B. 8) festgelegt und zu jedem Pixel wird 
festgelegt in welche dieser möglichen Richtungen der Gradient an dieser Stelle zeigt (die Gradientenrichtungen werden quantisiert). 

Dann wird das Bild in kleinere Blöcke unterteilt (z.B. 8x8 Pixel). Zu jedem Block wird nun für alle 
möglichen Gradientenrichtungen gezählt wieviele der Pixel in diese Richtung "zeigen". Es wird also für diesen Block
ein Histogram der vorkommenden Gradientenrichtungen erstellt. Um weniger sensibel gegenüber Bildrauschen zu sein werden
die Gradientenrichtungen mit ihrer jeweiligen Gradientenstärke gewichtet. 

HoG from Scratch - Die Webcam öffnen
------------------------------------

Wir beginnen wieder mit unserem Standard Loop und öffnen die Webcam. Wandeln Sie das Bild direkt in ein Graustufenbild (0 bis 255) und
`konvertieren <https://numpy.org/doc/stable/user/basics.types.html>`_ Sie den Datentyp in `np.float32` (0.0 bis 1.0). 

und rufen sie die noch zu 
implementierende Methode `process_hog` mit diesem Grauwertbild auf. Hier nocheinmal die Auflistung der Methoden die dir dabei helfen können:

* `cv2.VideoCapture <https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html>`_ – öffnet einen Video-Stream oder eine Kamera.
* `cv2.VideoCapture.read <https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1>`_ – liest einen Frame aus dem Stream.
* `cv2.VideoCapture.isOpened <https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#a9d2ca36789e7fcfe7a7be3b328038585>`_ – prüft, ob die Kamera geöffnet werden konnte.
* `cv2.cvtColor <https://www.geeksforgeeks.org/python-opencv-cv2-cvtcolor-method/>`_ – konvertiert Farbräume (z. B. in Graustufen).
* `cv2.waitKey <https://www.geeksforgeeks.org/python-opencv-waitkey-function/>`_ – wartet auf Tasteneingabe.


.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

      def process_hog(gray):
        pass
        
      if __name__ == "__main__":
        cap = cv2.VideoCapture(0)  
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # if frame is read correctly ret is True
            if not ret:
                exit()

            # Convert image to gray scale
            gray = np.float32(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.0)

            process_hog(gray)

            # Display the resulting frame
            if cv2.waitKey(1) == ord("q"):
                break

HoG from Scratch - Die Gradientenrichtungen
-------------------------------------------

Im ersten Schritt bestimmen wir zunächst die Richtungen der quantisierten Gradientenrichtungen. 
Dazu teilen wir das Intervall von 0 bis :math:`2\pi` in gleichmäßige Schritten ein. 

Verwenden Sie `numpy.linspace <https://numpy.org/doc/stable/reference/generated/numpy.linspace.html>`_ und schließen Sie den letzten Datenpunkt 
aus weil 0° Grad und 360° natürlich der selben Richtung entsprechen. Für z.B. 8 Gradientenrichtungen sollten Sie die folgenden Winkel finden

  .. code-block:: python
  
    winkel = [0.    0.785 1.571 2.356 3.142 3.927 4.712 5.498]

Zu einem konkreten Winkel :math:`\alpha` können wir die dazugehörige Gradientenrichtung :math:`\vec v` berechnen

.. math::

    \vec v(\alpha) = \begin{pmatrix}\cos(\alpha)\\ \sin(\alpha)\end{pmatrix}

Berechnen Sie nun für jeden der Winkel die dazugehörige Winkelrichtung und speichern Sie alle Winkel in einem :math:`2xN` array. Für z.B. 8 Gradientenrichtungen sollte 
ihre Array dann so aussehen

  .. code-block:: python

    directions = [[ 1.     0.707  0.    -0.707 -1.    -0.707 -0.     0.707]
                  [ 0.     0.707  1.     0.707  0.    -0.707 -1.    -0.707]]

Schreiben Sie eine Funktion `calculate_gradient_directions` welche zu einer Anzahl an Richtungen dieses dazugehörige Array zurückgibt. 


.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

      def calculate_gradient_directions(totalDirections = 12):
        angles = np.linspace(0, 2.0 * np.pi, totalDirections, endpoint=False)
        hogDirections = np.zeros((2,totalDirections))

        hogDirections[0, :] = np.cos(angles)
        hogDirections[1, :] = np.sin(angles)

        return hogDirections

HoG from Scratch - Gradienten und Gradientestärke
-------------------------------------------------

Nun implementieren wir die `process_hog` Methode. Berechnen Sie zunächst wieder für das Grauwertbild mit `cv2.Sobel <https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#gacea54f142e81b6758cb6f375ce782c8d>`_ 
die Gradienten in X und Y-Richtung. Verwenden Sie `ksize=5` und berechnen Sie die Gradientenstärke als 

.. math::

    \nabla I = \sqrt{I_x^2 + I_y^2}

Speichern Sie das Gradientenbild in X-Richtung als `gx`, das Gradientenbild in Y-Richtung als `gy` sowie
die Gradientstärke als `mag`.

.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

      def process_hog(gray, totalDirections = 12):
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=5)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
        mag = np.sqrt(gx**2 + gy**2)    

HoG from Scratch - Gradientenrichtung
-------------------------------------

Zur Bestimmung der Gradientenrichtung bestimmen wir das Skalarprodukt

.. math::

    \left(I_x,  I_y\right) \cdot \vec v(\alpha)

für alle möglichen Gradientenrichtungen und ordnen den Pixel derjenigen Richtung zu, wo
dieses Skalarprodukt maximal wird. Mathematisch berechnen wir also

.. math::

    \arg\max_j \left(I_x,  I_y\right) \cdot \vec v(\alpha_j) = 
    \arg\max_j \left(\cos(\alpha_j) I_x + \sin(\alpha_j) I_y\right)

für jeden Pixel. 

Um diese Berechnung zu vereinfachen, *flatten* Sie zunächst die Gradientenbilder `gx` und `gy` (`numpy.flatten <https://numpy.org/doc/2.1/reference/generated/numpy.ndarray.flatten.html>`_).
Erzeugen Sie dann gleichgroße neue Arrays `winningBin` und `bestDot` gefüllt mit nullen (`np.zeros_like <https://numpy.org/doc/2.2/reference/generated/numpy.zeros_like.html>`_)

Iterieren Sie über alle Gradientenrichtungen (rufen Sie Ihre Funktion `calculate_gradient_directions` auf um diese Richtungen zu bekommen) und berechnen Sie 
das Skalarprodukt (siehe oben). Bestimmen Sie diejenigen Einträge, bei denen das neue Skalarprodukt größer ist als das bisherige (vgl. mit `bestDot`)
und überschreiben Sie für diese Einträge sowohl `bestDot` (mit dem neuen, größeren Skalarprodukt) als auch `winningBin` mit dem Index des aktuell geprüften Bins. 

Am Ende erhalten Sie so zu jedem Pixel ihres Originalbildes denjenigen Index (Bin) der Gradientenrichtung, die am ehesten den tatsächlichen 
Gradienten des Pixels repräsentiert (in `winningBin`) sowie dessen Gradientenstärke (in `mag`). 

Damit `winningBin` wieder als Bild interpretiert werden kann `reshapen <https://numpy.org/doc/stable/reference/generated/numpy.reshape.html>`_ sie das Bild wieder auf die Größen des originalen Grauwertbildes.

.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

      def process_hog(gray, totalDirections = 12):
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=5)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
        mag = np.sqrt(gx**2 + gy**2)    

        gx, gy = gx.flatten(), gy.flatten()
        winningBin, bestDot = np.zeros_like(gx), np.zeros_like(gx)
        for direction in range(totalDirections):
          dot = gx * hogDirections[0, direction] + gy * hogDirections[1, direction]

          greaterIndices = dot > bestDot
          winningBin[greaterIndices] = direction
          bestDot[greaterIndices] = dot[greaterIndices]

        winningBin = winningBin.reshape(gray.shape) 

HoG from Scratch - Gradientenrichtungen anzeigen
------------------------------------------------

Es macht Sinn diese Gradientenrichtungen konkret anzuzeigen um ein 
Gefühl für die so kodierte Information zu bekommen. Wandeln Sie dazu das `winningBin` Bild zunächst
in ein Grauwertbild zurück indem Sie den Bereich der möglichen Bins :math:`[0,\dots,N-1]` linear auf den Bereich :math:`[0,\dots,255]` 
abbilden. Wandeln Sie auch den Datentypen zurück in einen `np.uint8`. Verwenden Sie dann 
`cv2.applyColoMap <https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html>`_ um das Bild geeignet einzufärben (z.B. mit der `cv2.COLORMAP_JET` Farbskala) und zeigen Sie es mit 
`cv2.imshow <https://www.geeksforgeeks.org/python-opencv-cv2-imshow-method/>`_ an. Es kann für die Anzeige Sinn machen zu schwache Gradienten
zu unterdrücken. Setzen Sie daher in ihrem Farbbild alle Pixel auf :math:`(0,0,0)`, für welche die Gradientestärke geringen als 1.5 ist. 

Ihr Bild sollte dann in etwa so aussehen (bei 12 Histogrambins):

.. image:: ./gradientdirections.png
   :alt: Gradientenrichtungsbild
   :width: 400px
   :align: center



.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

      def process_hog(gray, totalDirections = 12):
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=5)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
        mag = np.sqrt(gx**2 + gy**2)    

        gx, gy = gx.flatten(), gy.flatten()
        winningBin, bestDot = np.zeros_like(gx), np.zeros_like(gx)
        for direction in range(totalDirections):
          dot = gx * hogDirections[0, direction] + gy * hogDirections[1, direction]

          greaterIndices = dot > bestDot
          winningBin[greaterIndices] = direction
          bestDot[greaterIndices] = dot[greaterIndices]

        winningBin = winningBin.reshape(gray.shape) 

        binGray = np.uint8(255 * winningBin / (totalDirections - 1))
        binColor= cv2.applyColorMap(binGray, cv2.COLORMAP_JET)
        binColor[mag < 1.5] = (0, 0, 0)

        cv2.imshow("Gradient Direction", binColor)

HoG from Scratch - Der Feature-Vektor
-------------------------------------

Implementieren Sie nun eine Methode `hog_cell`. Diese soll das Magnituden-Bild `mag`, die dominanten Gradientenrichtungen `winningBin`
sowie die Anzahl der Gradientenrichtungen erhalten. Eine geeignete Signatur dieser Methode könnte so aussehen:

.. code-block:: python

    def hog_cell(magnitude, winningBin, totalDirections):

Das Ziel ist es hier für die übergebenen Bilder (später: Bildausschnitte) das Histogram der 
Gradientenrichtungen zu berechnen und als normierten Feature-Vektor zurückzugeben. Wenn wir also :math:`N` Gradientenrichtungen haben geben wir einen 
:math:`N`-dimensionalen Featurevektor zurück, welcher für jede prinzipielle Richtung der Summe der jeweiligen Gradientenstärken enthält. Mathematisch berechnen wir also

.. math::

    \textbf{h} = \left(h_0, h_1, \dots, h_n\right)

mit 

.. math::

    h_j = \sum_{winningBin(x,y) = j} mag(x,y)

**Achtung**: Im Orignalpaper wird der HoG-Featurevektor über mehrere Zellen normalisiert. Wir weichen hier von dieser Implementierung ab und dividieren
den Vektor einfach nur durch eine Konstante (in diesem Fall: 256).


.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

      def hog_cell(magnitude, winningBin, totalDirections):
        cellVector = np.zeros(totalDirections)
        for index in range(totalDirections):
          cellVector[index] = magnitude[winningBin == index].sum()
    
        return cellVector / 256.0

HoG from Scratch - Visualisierung einer HoG-Zelle
-------------------------------------------------

Um eine einzelne HoG-Zelle zu visualisieren zeichnen wir für jede der Gradientenrichtungen einen stilisierten Vektorpfeil. Als Helligkeitsintenstät des
Pfeils verwenden wir die akkumulierte Gradientenstärek. Schreiben Sie eine Methode `visualize_hog_cell` welche den gerade berechneten HoG-Vektor, 
das Array mit Gradientenrichtungsvektoren sowie die Größe der zu zeichnenden Zelle (Breite und Höhe) erhält. Eine geeignete Signatur dieser Methode könnte also so aussehen:

.. code-block:: python

    def visualize_hog_cell(cellVector, directions, shape=(16,16)):
  
Diese Methode soll ein entsprechend der angegebenen Zellengröße dimensioniertes Grauwertbild zurückgeben. Erzeugen Sie dieses Bild indem Sie mit `np.zeros <https://numpy.org/devdocs/reference/generated/numpy.zeros.html>`_ eine
passend dimensionierte Matrix gefüllt mit nullen erzeugen. Iterieren Sie dann über alle Einträge des `cellVector` und bestimmen Sie die dazugehörige Gradientenrichtung anhand des 
ebenfalls übergebenen `directions`-Array. Nutzen Sie `cv2.line <https://www.geeksforgeeks.org/python-opencv-cv2-line-method/>`_ um ausgehend von der Mitte des Bildes ein Linie in diese Richtung zu 
zeichnen. Skalieren Sie den Richtungsvektor :math:`(dx,dy)` passend zur (halben) Zellengröße und wählen Sie die akkumulierte Gradientenstärke aus dem `cellVector` als Farbe für die Linie. 

Geben Sie schließlich das Bild zurück. 

.. admonition:: Lösung anzeigen
   :class: toggle

   .. code-block:: python

      def visualize_hog_cell(cellVector, directions, shape=(16,16)):
        cell = np.zeros(shape)
        W, H = shape[0], shape[1]
        for index, value in enumerate(cellVector):
          dx, dy = directions[0, index], directions[1, index]

          x0, y0 = int(W // 2), int(H // 2)
          x1, y1 = int(x0 + dx * W / 2), int(y0 + dy * H / 2)
          cv2.line(cell, (x0, y0), (x1, y1), (value, value, value))

        return cell

HoG from Scratch - Berechnen der Features über das ganze Bild
-------------------------------------------------------------

Wir wollen das Bild nun in Zellen der Größe :math:`(12x12)` Pixel unterteilen. Für jede dieser Zelle schneiden wir den entsprechenden Abschnitt aus dem `winningBin`- und dem `mag`-Bild aus, rufen die 
gerade implementierte `hog_cell`-Methode auf um den Featurevektor zu bestimmen und lassen diesen mit der `visualize_hog_cell`-Methode zeichnen. Die entstehenden Einzelbilder kopieren wir zusammen in 
ein großes Bild und zeigen dieses ebenfalls an. Eine entsprechende Implementierung könnte z.B. so aussehen

  .. code-block:: python

    cellSize = 8
    hogImage = np.zeros_like(gray)
    for x0 in range(0, gray.shape[1], cellSize):
      for y0 in range(0, gray.shape[0], cellSize):
          x1, y1 = x0 + cellSize, y0 + cellSize

          cellVector = hog_cell(mag[y0:y1, x0:x1], winningBin[y0:y1, x0:x1], totalDirections)
          hogImage[y0:y1, x0:x1] = visualize_hog_cell(cellVector, hogDirections, (cellSize, cellSize))

    
    cv2.imshow("HOG Vector", hogImage)

HoG from Scratch - Musterlösung
-------------------------------

:doc:`source`
