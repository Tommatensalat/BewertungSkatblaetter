# BewertungSkatblaetter
Beinhaltet den Praktischen Teil zur Jugend Forscht Arbeit "Der Vergleich von lernenden und nicht-lernenden Algorithmen anhand des Spiels Skat
Im "master"-Branch kann der Programmcode entnommen werden

!Vorher bitte die Readme lesen!

Wenn Sie überprüfen wollen, ob die Ergebnisse aus der Arbeit stimmen, dann öffnen Sie die "verifying.py".
In Zeile 83, können Sie den Grad und die Anzahl der einbezogenen Trainingsdaten anpassen. Der jeweils optimale Wert für den Regularisierungskoeffizienten richtet sich automatisch danach.
Das Ergebnis des Naiven Algorithmus wird ebenfalls automatisch anschließend angegeben.

Aus der "model.py" kann entnommen werden, wie die KI nach den optimalen Parameterwerten sucht. Wichtig sind hierbei die Funktionen die "read_datas()"-Methode und die anschließende "method()"-Methode 

Wird die "main.py" gestartet kann die Stärke der MCTS in einer Oberfläche beobachtet werden zur Generierung der Trainingsdaten.

In "players.py" ist die Berechnung durch den Naiven Algorithmus enthalten. Dies wird in der "calculate_power_of_algorithm()"-Methode umgesetzt. Die weiteren Methoden, die dort nicht aufgerufen werden, sind Hilfsmethoden bzw. werden sie aufgerufen beim Spielen. Die Klasse "MCTS_Node" beinhaltet die gesamte Berechnung des besten Zuges beim Spielen, ist demnach die Implementierung der Monte-Carlo-Tree-Search.

Die Datei "game.py" umfasst die Spielregeln und Bedingungen.

Um eine bessere Vorstellung von den Bewertungen der Algorithmen zu erhalten, dann ist dies über die "comparing.txt"-Datei möglich. Dort werden 20 Blätter aus dem Testdatensatz von beiden Algorithmen bewertet. Die Implementierung dazu befindet sich in der "rating.py".


Folgende Bibliotheken müssen implementiert werden:
numpy, insbesondere genfromtxt
tkinter
random
collections
time
scipy
seaborn
sklearn, insbesondere svm
sklearn.model_selection, insbesondere train_test_split
