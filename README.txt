Victor FLEISER


Notes importantes :
/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
Mon programme manipule la taille/position/couleur de la fenêtre constament pour un effet de style, si le programme pose problème sur le système d'éxploitation il est possible de désactiver le mouvement/redimensionnement en changeant la variable booléene dans TP1_global_variables
/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\


Autres notes :

- Il est également possible de modifier le nombre de personnages initialement dans le même fichier

- Les commentaire et noms de variables sont souvent un mix de Francais / Anglais, j'ai essayé de tout retraduire en Francais mais c'est possible que j'ai oublié certains commentaire/variables

- Le programme n'a été testé que sur 1 version de MAC et Windows, je n'ai aucune idée comment Linux et les machines virtuelles vont intéragir avec le placement/déplacement/redimensionnement de fenêtres (cf ci-dessus si sa pose problème)
Le programme est le plus agréable à l'oeuil sur MAC pour info

- A la base je comptais avoir du texte coloré, et donc j'ai codé la plupart du code pré-tkinter avec des fonctions ajoutant des Ansi Escape Code au chaines de caractères pour colorer le texte, mais j'ai découvert que cela ne fonctionne que sur terminal, ignorer toute fonction colorant du texte dans TP1_classes_persos


- Il y a 2 modes visuels secrets :
	
	- Le mode DVD screensaver : la fenêtre rebondit sur les bords de l'écran
	
	- Le mode Rainbow : la fenêtre change constament de couleur de fond d'écran

Ces modes sont purement pour le fun et sont activables en terminant le jeu ou en insérant un code secret (cf : TP1_GUI.py activate_secret_options())
Par contre il est possible de créer des bugs non pris en charge en utilisant ces modes secrets


- Bugs connus :
	
	- Double clicker (rapidement) sur un personnage va le sélectionner puis déséléctionner dans le code, par contre le visuel ne le fera que 1 fois, créant ainsi un décallage entre visuel et réel jusqu'à la prochaine mise à jour des list box
	
	- Clicker exactement entre 2 personnages va en sélectionner un/aucun aléatoirement visuellement mais pas forcément le personnage correct dans le code
	
	- Si le barbare se tue soit même en attaquant par self damage, alors il sera encore disponible à sélectionner dans la liste le temps du tour de l'adversaire, il mourra automatiquement à la fin du tour de l'adversaire
