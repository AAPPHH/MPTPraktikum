.. _webcam:

Die Webcam - Einfache Bildnormalisierungen
==========================================

Mit OpenCV ist es recht einfach die Webcam zu öffnen. 

Aufgabe 1: Ein Bild von der Webcam anzeigen
----------------------------------------------

Öffnen Sie einen s.g. `VideoCapture <https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html>`_, 
lesen Sie ein Bild von der Webcam mit der `read <https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1>`_-Methode und zeigen Sie dieses 
mit `cv2.imshow <https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1>`_ an. Übergeben Sie dann 
die Kontrolle an das Betriebssystem damit es das Fenster mit dem Bild zeichnen kann indem Sie 
`cv2.waitKey <https://www.geeksforgeeks.org/python-opencv-waitkey-function/>`_ aufrufen. Rufen Sie `cv2.waitKey` mit dem Parameter 0 auf 
um unendlich lange auf einen Tastendruck zu warten 

.. code-block:: python 

    cv2.waitKey(0)


.. admonition:: Lösung anzeigen
  :class: toggle

  .. code-block:: python 

      cap = cv2.VideoCapture(0)  
      if not cap.isOpened():
          print("Cannot open camera")
          exit()

      ret, frame = cap.read()
      cv2.imshow("Kamerabild", frame)
      cv2.waitKey(0)

Aufgabe 2: Eine sinnvolle Endloßschleife
----------------------------------------

Um immer wieder ein neues Bild von der Webcam zu lesen macht es Sinn das lesen des Bildes (`read <https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1>`_) 
sowie das Anzeigen in einer Endloßschleife durchzuführen. Diese können Sie recht leicht beginnen mit

.. code-block:: python

    while True:

Warten Sie nur 1 Millisekunde und beenden Sie das Programm, wenn der Benutzer die Taste `q` drückt. 

.. admonition:: Lösung anzeigen
  :class: toggle

  .. code-block:: python 

      cap = cv2.VideoCapture(0)  
      if not cap.isOpened():
          print("Cannot open camera")
          exit()

      while True:
        ret, frame = cap.read()
        cv2.imshow("Kamerabild", frame)
        if cv2.waitKey(1) == ord('q'):
          break

Aufgabe 3: Grauwertbilder und Histogramme
-----------------------------------------         

OpenCV verwendet im Unterbau die bekannte numpy-Bibliothek, so sind z.B. die Bilder stets NumPy-Arrays. 

Sie können das Bild von der Webcam leicht in ein Grauwertbild umrechnen. Verwenden Sie dazu die Methode 
`cv2.cvtColor <https://www.geeksforgeeks.org/python-opencv-cv2-cvtcolor-method/>`_ mit dem Parameter `cv2.COLOR_BGR2GRAY`.

Implementieren Sie dann eine Methode

.. code-block:: python 

    def drawHistogram(gray):

welche das Grauwertbild erhält und ein neues Bild mit dem Histogram der Grauwerte zeichnet. 

Verwenden Sie dazu zunächst `np.histogram <https://numpy.org/doc/2.2/reference/generated/numpy.histogram.html>`_ und übergeben Sie mit `range(256)` konkrete Grenzen für die Histogram-Bins. 
Sie benötigen nur den ersten der beiden Rückgabewerte, der zweite kann ignoriert werden. Wandeln Sie das Histogramm in einen 
`np.float32 <https://numpy.org/doc/stable/user/basics.types.html>`_ um und normieren Sie das Histogram, indem Sie durch den höchsten vorkommenden Wert teilen. 

Hinweis: Diesen können Sie mit `np.max <https://numpy.org/doc/2.2/reference/generated/numpy.max.html>`_ relativ leicht finden. 

Nun zeichen wir das Histogramm als Balkendiagramm. Erzeugen Sie dazu ein Bild der Größe (128 x 256) gefüllt mit Nullen (verwenden Sie `np.zeros <https://numpy.org/devdocs/reference/generated/numpy.zeros.html>`_).
Iterieren Sie über alle Einträge im Histogram und verwenden Sie `cv2.line <https://www.geeksforgeeks.org/python-opencv-cv2-line-method/>`_ um eine vertikale Linie (den Balken) in dem Bild zu zeichen.
Verwenden Sie den Index des Bins als X-Koordinate. Verwenden Sie den Wert des Histogramms als Höhe des Balkens. Rechnen Sie Anfangs- und Endkoordinate entsprechend aus und zeichen sie. 

Geben Sie das Bild zurück ohne es anzuzeigen.
Hinweis: Sie können ihre Hauptschleife im Programm so anpassen, das Sie zu jedem Kamerabild auch das Histogram des Grauwertbildes berechnen 
und dieses dann ebenfalls anzeigen. 

.. admonition:: Lösung anzeigen
  :class: toggle

  .. code-block:: python 

      def drawHistogram(gray):
        hist, _ = np.histogram(gray, bins=range(256))
        hist = np.float32(hist)
        hist = hist / np.max(hist)

        H = 128
        histImage = np.zeros((H, 256))
        for bin, value in enumerate(hist):
            x0, y0 = bin, H
            x1, y1 = bin, int(H * (1.0 - value))
            cv2.line(histImage, (x0, y0), (x1, y1), bin / 256.0, 1)

        return histImage

Aufgabe 4: Helligkeit und Kontrast normalisieren
------------------------------------------------  

Schreiben Sie eine Methode `adjustBrightness` mit folgender Signatur

.. code-block:: python 

  def adjustBrightness(gray, brightness, contrast):

Berechnen Sie mit `np.mean <https://numpy.org/doc/2.2/reference/generated/numpy.mean.html>`_ und 
`np.std <https://numpy.org/doc/stable/reference/generated/numpy.std.html>`_ Mittelwert (:math:`\mu`) und Standardabweichung (:math:`\sigma`) des Grauwertbildes.

Normieren Sie dann die Grauwerte des Bildes derart, das diese den mit `brightness` übergeben Mittelwert und die mittels `contrast` übergebene 
Standardabweichung haben. Diese Normalisierung erreichen Sie, indem Sie setzen

.. math:: 

  I = brightness + contrast \cdot \frac{I - \mu}{\sigma}

Verwenden Sie `np.clip <https://numpy.org/doc/2.1/reference/generated/numpy.clip.html>`_ um die Werte im Bereich zwischen 0.0 und 1.0 zu begrenzen (abzuschneiden) 
und wandeln Sie das Bild in in `np.uint8`-Bild um. Multiplizieren Sie vorher mit 255.0 um dem neuen Datenbereich gerecht zu werden. 

.. admonition:: Lösung anzeigen
  :class: toggle

  .. code-block:: python 

    def adjustBrightness(gray, brightness, contrast):
        mean, std = np.mean(gray), np.std(gray)

        norm = brightness + contrast * (gray - mean) / std
        return np.uint8(np.clip(norm, 0.0, 1.0) * 255.0)

Aufgabe 5 - Interaktion
-----------------------

Passen Sie ihre Hauptschleife so an, dass Sie zu jedem Bild das Grauwertbild berechnen und dieses 
mit der Methode `adjustBrightness` normalisieren (:math:`\mu = 0.5, \sigma = 0.5`). 
Zeigen Sie dann beide Bilder inklusive dem dazugehörige Grauwerthistogram an. Machen Sie die gewünschte 
Brightness sowie den gewünschten Kontrast Variabel und verändern Sie die Zielgröße basierend auf der vom Benutzer gedrückten Taste.
Sie können z.B. mit **+** und **-** den Kontrast erhöhen bzw. verringer sowie mit **1** und **2** die Helligkeit. 


.. admonition:: Lösung anzeigen
  :class: toggle

  .. code-block:: python 

    brightness = 0.5
    contrast = 0.1

    while True:
      # Capture frame-by-frame
      ret, frame = cap.read()

      # if frame is read correctly ret is True
      if not ret:
          exit()

      cv2.imshow("Kamerabild", frame)

      gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
      cv2.imshow("Graubild", gray)
      cv2.imshow("Graubild - Histogramm", drawHistogram(gray))

      norm = adjustBrightness(gray, brightness, contrast)
      cv2.imshow("Normalisiert", norm)
      cv2.imshow("Normalisiert - Histogramm", drawHistogram(norm))

      key = cv2.waitKey(1)
      if key == ord("+"):
          contrast = np.clip(contrast + 0.01, 0.0, 1.0)
      
      if key == ord("-"):
          contrast = np.clip(contrast - 0.01, 0.0, 1.0)

      if key == ord("1"):
          brightness = np.clip(brightness - 0.05, 0.0, 1.0)
      
      if key == ord("2"):
          brightness = np.clip(brightness + 0.05, 0.0, 1.0)

      if key == ord("q"):
          break

WebCam - Musterlösung
---------------------

:doc:`source`